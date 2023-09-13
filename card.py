import subprocess
import os
import re
from helpers import ImageMagickCommandBuilder
IM = ImageMagickCommandBuilder

# TODO: Red Emissions (Ijiraq needs its red eyes!), Ijiraq versions of cards, and proper portrait of Stinkbug_Talking.

class Card:
    original_card_height = 190 # px
    fullsize_card_height = 1050 # px
    scale = fullsize_card_height / original_card_height
    def __init__(self, cursor, base, card_data, tribe_data, sigil_data, flag_data,
                 before_decal_data, decal_data, deathcard_data, staticon_data):
        # Establish base directory
        self.base = base + 'resource'
        # Gain access to database
        self.cursor = cursor

        # Establish card data
        for key, value in card_data.items():
            setattr(self, key, value)

        # Establish tribe data
        self.tribes = self.establish_attribute_data(tribe_data, 'tribe')
        self.tribes = self.preserve_tribe_order()
        # Establish sigil data
        # TODO: Preserve sigil priority for card
        sorted_sigil_data = sorted(sigil_data, key = lambda x: x['priority'])
        self.sigils = [item['sigil_filename'] for item in sorted_sigil_data]
        # Establish flag data
        self.flags = self.establish_attribute_data(flag_data, 'flag')
        # Establish decal data
        self.decals = self.establish_attribute_data(decal_data, 'decal')
        self.before_decals = self.establish_attribute_data(before_decal_data, 'before_decal')
        # Establish deathcard data
        self.deathcard = deathcard_data
        # Establish staticon data
        self.staticon = self.establish_attribute_data(staticon_data, 'staticon')
        # Get terrain layout offset
        self.terrain_layout_x_offset = self.get_terrain_layout()

    def establish_attribute_data(self, data, data_type):
        attributes = []
        for row in data:
            attributes.append(row[f'{data_type}_filename'])
        return attributes
    def get_notes_from_database(self):
        # TODO: Function needs rewriting due to the changes made in the database. Will do when it becomes necessary.
        # # SELECT query and fetch to retrieve notes based on note_id
        # self.cursor.execute('SELECT description, mechanics, gmNotes FROM notes WHERE id = ?', (self.note_id,))
        # row = self.cursor.fetchone()
        # # Assign notes to card
        # if row:
        #     description, mechanics, gmNotes = row
        #     return {
        #         'description': description,
        #         'mechanics': mechanics,
        #         'gmNotes': gmNotes
        #     }
        # else:
        #     return None
        pass
    def get_terrain_layout(self):
        if self.rarity == 'terrain' and 'no_terrain_layout' not in self.flags:
            return -70
        else:
            return 0
    def preserve_tribe_order(self):
        '''Tribe order is determined by the tribe table's priority in the database.'''
        self.cursor.execute('SELECT filename FROM tribes ORDER BY priority')
        rows = self.cursor.fetchall()
        ordered_tribes = []
        for row in rows:
            if row[0] in self.tribes:
                ordered_tribes.append(row[0])
        return ordered_tribes

    def generate_card_image(self):
        im = self.initialize_image_builder()
        im = self.add_card_background(im)
        im = self.add_decals(im, 'before')
        im = self.add_card_portrait(im)
        # Resize
        im.resize(None, self.fullsize_card_height) # 1050 pixels @ 300 dpi = 3.5 inches
        # Set default gravity
        im.gravity('NorthWest')
        im = self.add_tribes(im)
        im = self.add_card_cost(im)
        im = self.add_health(im)
        im = self.add_special_stat_icons(im)
        im = self.add_sigils(im)
        im = self.add_squid_title(im)
        im = self.add_card_name(im)
        im = self.add_long_elk_decal(im)
        im = self.add_card_border(im)
        im = self.add_card_bleed(im)
        im = self.apply_emission_effects(im)
        im = self.add_decals(im, 'after')
        im = self.add_golden_effect(im)
        return self.generate_image_buffer(im)

    def initialize_image_builder(self):
        directory = f'{self.base}/fonts'

        im = IM()
        im.font(f'{directory}/HEAVYWEIGHT.otf')
        im.pointsize(200)
        im.background('None')
        im.filter('Box')
        return im

    def add_card_background(self, im):
        directory = f'{self.base}/cards'
        background_path = f'{directory}/{self.temple}_{self.rarity}.png'
        im.resource(background_path)
        return im

    def add_card_portrait(self, im):
        if 'no_portrait' not in self.flags:
            if 'base_death_card' in self.flags:
                im = self.add_base_death_card(im)
            else:
                im = self.add_portrait(im)
        return im

    def add_portrait(self, im):
        directory = f'{self.base}/portraits'
        im.resource(f'{directory}/{self.filename}.png')
        im.gravity('Center')
        im.geometry(1, -15)
        im.composite()
        return im

    def add_base_death_card(self, im):
        directory = f'{self.base}/deathcards/base'
        # Body
        dc = IM(f'{directory}/{self.deathcard["body"]}.png')
        dc.gravity('NorthWest')
        # Head
        dc.resource(f'{directory}/heads/{self.deathcard["head"]}.png')
        dc.composite()
        # Mouth
        dc.resource(f'{directory}/mouth/{self.deathcard["mouth"]}.png')
        dc.geometry(40, 68).composite()
        # Eyes
        dc.resource(f'{directory}/eyes/{self.deathcard["eyes"]}.png')
        dc.geometry(40, 46).composite()
        if self.deathcard["lost_eye"] == 'True':
            dc.parens(
                IM().command('xc:black[17x17]').geometry(40, 46)).composite()
        im.parens(dc).gravity('Center').geometry(1, -15).composite()
        return im

    def add_tribes(self, im):
        directory = f'{self.base}/tribes'
        # TODO: Not sure how it works with cards with 2 to 3 tribes (but not all of them)
        tribePositions = [[-12, 3], [217, 5], [444, 7], [89, 451], [344, 452]]
        for i, tribe in enumerate(self.tribes):
            tribeLocation = f'{directory}/{tribe}.png'
            position = tribePositions[i]
            im.parens(IM(tribeLocation)
                      .resize(None, 354)
                      .gravity('NorthWest')
                      .alpha('Set')
                      .command('-channel', 'A', '-evaluate', 'multiply', '0.4', '+channel')
            )
            im.geometry(position[0], position[1])
            im.composite()
        return im

    def add_card_cost(self, im):
        directory = f'{self.base}/costs'
        cost_path = None
        for var, value in vars(self).items():
            if var == 'cost':
                if value is None or value == 'None':
                    return im
                elif value[0] != '[':
                    cost_path = f'{directory}/{value}.png'
                    im.parens(
                        IM(cost_path)
                        .interpolate('Nearest')
                        .filter('Point')
                        .resize(284)
                        .filter('Box')
                        .gravity('East')
                    ).gravity('NorthEast')
                    im.geometry(32, 110)
                    im.composite()

                    im.gravity('NorthWest')
                else:
                    costs = re.findall(r'\[(.*?)\]', value)
                    if len(costs) > 2:
                        cost_path =f'{directory}/long_cost.png'
                    else:
                        cost_path =f'{directory}/short_cost.png'
                    base = IM(cost_path)
                    base.gravity('NorthWest')
                    for i, cost in enumerate(costs):
                        gem_path = f'{directory}/{cost}.png'
                        base.resource(gem_path)
                        location = (19, 1) if i == 0 else (7, 1) if i == 1 else (-5, 1) if i == 2 else (-17, 1) if i == 3 else (-29, 1)
                        base.geometry(*location).composite()
                    im.parens(
                        base
                        .interpolate('Nearest')
                        .filter('Point')
                        .resize(284)
                        .filter('Box')
                        .gravity('East')
                    ).gravity('NorthEast')
                    im.geometry(32, 110)
                    im.composite()

                    im.gravity('NorthWest')
                    #for cost in costs:
        return im

    def add_health(self, im):
        if 'hide_power_and_health' not in self.flags:
            healthWidth = 114
            healthHeight = 215
            im.parens(
                IM()
                .pointsize(209)
                .size(healthWidth, healthHeight)
                .label(self.health)
                .gravity('East')
                .extent(healthWidth, healthHeight)
            ).gravity('NorthEast').geometry(32 - self.terrain_layout_x_offset, 815).composite()

        return im

    def add_special_stat_icons(self, im):
        # TODO: Will need to change this code if there's ever a staticon implemented to replace health
        # As of now, calling self.staticon[0] is acceptable because it's never expected for a card to have
        # more than 1 staticon. It's always assumed to be a replacement for power.
        directory = f'{self.base}/staticons'
        if self.staticon:
            im.parens(
                IM(f'{directory}/{self.staticon[0]}.png')
                .interpolate('Nearest')
                .filter('Point')
                .resize(245)
                .filter('Box')
                .gravity('NorthWest')
            ).geometry(5, 705).composite()
        elif self.power is not None:
            drawPower = not (
                (self.power == 0 and (self.rarity == 'terrain' and 'no_terrain_layout' not in self.flags)) or 'hide_power_and_health' in self.flags)
            if drawPower:
                w = 114
                h = 215
                im.parens(
                    IM()
                    .pointsize(209)
                    .size(w, h)
                    .gravity('West')
                    .label(self.power)
                    .extent(w, h)
                ).gravity('NorthWest').geometry(68, 729).composite()

        return im

    def add_sigils(self, im):
        directory = f'{self.base}/sigils'
        if self.sigils:
            if len(self.sigils) == 1:
                sigil_path = f'{directory}/{self.sigils[0]}.png'
                im.parens(
                    IM(sigil_path)
                    .interpolate('Nearest')
                    .filter('Point')
                    .resize(None, 253)
                    .filter('Box')
                ).gravity('NorthWest').geometry(221 + self.terrain_layout_x_offset, 733).composite()
            elif len(self.sigils) == 2:
                sigil_path1 = f'{directory}/{self.sigils[0]}.png'
                sigil_path2 = f'{directory}/{self.sigils[1]}.png'
                im.filter('Box')
                im.parens(
                    IM(sigil_path1)
                    .resize(None, 180)
                ).gravity('NorthWest').geometry(180 + self.terrain_layout_x_offset, 833).composite()
                im.parens(
                    IM(sigil_path2)
                    .resize(None, 180)
                ).gravity('NorthWest').geometry(331 + self.terrain_layout_x_offset, 720).composite()
            # TODO: Must implement 3 and 4 sigils on a card at some point!
            # elif len(sigils) == 3:
            #     pass
            # elif len(sigils) == 4:
            #     pass

        return im

    def add_squid_title(self, im):
        directory = f'{self.base}/misc'
        if 'squid' in self.flags:
            squid_title_path = f'{directory}/squid_title.png'
            im.parens(
                IM(squid_title_path)
                .interpolate('Nearest')
                .filter('Point')
                .resize(None, 152)
                .filter('Box')
                .gravity('North')
                .geometry(0, 20)
            ).composite()

        return im
#
    def add_card_name(self, im):
        directory = f'{self.base}/fonts'
        if self.name and 'squid' not in self.flags:
            # Default for english
            size = {'w': 570, 'h': 155}
            position = {'x': 0, 'y': 18}
            locale = 'en' # Change this for a different language
            if locale == 'ko':
                im.font(f'{directory}/Stylish-Regular.ttf')
                position = {'x': 4, 'y': 34}
            elif locale in ('jp', 'zh-cn', 'zh-tw'):
                if locale == 'jp':
                    font = 'ShipporiMincho-ExtraBold.ttf'
                elif locale == 'zh-cn':
                    font = 'fonts/NotoSerifSC-Bold.otf'
                elif locale == 'zh-tw':
                    font = 'fonts/NotoSerifTC-Bold.otf'
                size = {'w': 570, 'h': 166}
                position = {'x': 0, 'y': 16}
                im.font(f'{directory}/{locale}')
            im.parens(
                IM()
                .pointsize()
                .size(size['w'], size['h'])
                .background('None')
                .label(self.name)
                .trim()
                .gravity('Center')
                .extent(size['w'], size['h'])
                .resizeExt(lambda g: g.scale(106, 100).flag('!'))
            ).gravity('North').geometry(position['x'], position['y']).composite().font(f'{directory}/HEAVYWEIGHT.otf')

        return im
    def add_long_elk_decal(self, im):
        directory = f'{self.base}/decals'
        if 'snelk' in self.decals:
            long_elk_decal_path = f'{directory}/snelk.png'
            im.parens(
                IM(long_elk_decal_path)
            ).resize(None, self.fullsize_card_height).gravity('Center').geometry(1, 0).composite()
        return im
    def add_card_border(self, im):
        directory = f'{self.base}/cardbackgrounds'
        background_path = f'{directory}/{self.temple}_{self.rarity}.png'
        if 'card_border' in self.flags:
            background = IM(background_path).resize(813, 1172)
            im.gravity('Center')\
                .extent(813, 1172)\
                .parens(background)\
                .compose('DstOver')\
                .composite()\
                .compose('SrcOver')
        return im
    def add_card_bleed(self, im):
        directory = f'{self.base}/cardbackgrounds'
        background_path = f'{directory}/{self.temple}_{self.rarity}_bleed.png'
        if 'card_bleed' in self.flags:
            background = IM(background_path).resize(891, None)
            im.gravity('Center')\
                .extent(853, 1178)\
                .parens(background)\
                .compose('DstOver')\
                .composite()\
                .compose('SrcOver')
        return im
    def apply_emission_effects(self, im):
        # TODO: Add red emission effects
        directory = f'{self.base}/emissions'
        if 'emission' in self.flags and 'golden' not in self.flags:
            emission_path = f'{directory}/{self.filename}.png'
            if os.path.exists(emission_path):
                for i in [False, True]:
                    emission = IM(emission_path).command('-fill', 'rgb(161,247,186)', '-colorize', '100').resizeExt(lambda g: g.scale(self.scale * 100)).gravity('Center').geometry(3, -15 * self.scale)
                    if i == True:
                        emission.command('-blur', '0x10')
                    im.parens(emission).composite()
        return im

    def add_golden_effect(self, im):
        directory = f'{self.base}/emissions'
        if 'emission' in self.flags and 'golden' in self.flags:
            im.parens(
                IM().command('-clone', '0', '-fill', 'rgb(255,128,0)', '-colorize', '75')
            ).geometry(0, 0).compose('HardLight').composite()

            emission_path = f'{directory}/{self.filename}.png'
            if emission_path and os.path.exists(emission_path):
                im.parens(
                    IM(emission_path)
                    .filter('Box')
                    .resizeExt(lambda g: g.scale(self.scale * 100))
                    .gravity('Center')
                    .geometry(0, -15 * self.scale)
                ).compose('Overlay').composite()

        return im
    def add_decals(self, im, when):
        # TODO: Add a helper function that gives priority to certain decals. Add a column to decal table for priority!
        directory = f'{self.base}/decals'
        if when == 'after' and self.decals:
            for decal in self.decals:
                if decal != 'snelk':
                    decal_path = f'{directory}/{decal}.png'
                    im.parens(
                        IM(decal_path)
                        .filter('Box')
                        .resize(None, self.fullsize_card_height)
                    ).gravity('Center').composite()
        elif when == 'before' and self.before_decals:
            for decal in self.before_decals:
                if decal != 'snelk':
                    decal_path = f'{directory}/{decal}.png'
                    im.parens(
                        IM(decal_path)
                        .filter('Box')
                    ).gravity('Center').composite()
        return im



    def generate_image_buffer(self, im):
        return buffer_from_command_builder(im)

def buffer_from_command_builder(im, input_data=None, filetype='PNG'):
    command_args = ['magick'] + im.parts() + [f'{filetype}:-']
    command = ' '.join(command_args)
    print(command)
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = process.communicate(input=input_data)

    if process.returncode != 0:
        print(f"ImageMagick Error: {stderr.decode('utf-8')}")
        #raise RuntimeError(f"ImageMagick Error: {stderr.decode('utf-8')}")

    return stdout