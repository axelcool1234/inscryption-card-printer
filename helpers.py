import sqlite3
from typing import Optional, Callable, Union, List

# Decorator for database connection handling
def db_connect(func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('database/inscryption.db')
        cursor = conn.cursor()
        result = func(cursor, *args, **kwargs)
        conn.close()
        return result
    return wrapper

class Geometry:
    def __init__(self):
        self._offset = None
        self._flag = None
        self._data = None

    def offset(self, x: Optional[int] = None, y: Optional[int] = None) -> 'Geometry':
        if x is None and y is None:
            self._offset = None
        elif isinstance(x, int) and isinstance(y, int):
            self._offset = {'x': x, 'y': y}
        else:
            raise ValueError(f"Invalid parameters for offset '{x},{y}'")
        return self

    def flag(self, flag: str) -> 'Geometry':
        available_flags = ['^', '!', '<', '>', '#']
        if flag not in available_flags:
            raise ValueError(f"Invalid flag '{flag}'")
        self._flag = flag
        return self

    def size(self, width: Optional[int] = None, height: Optional[int] = None) -> 'Geometry':
        if width is None and height is None:
            self._data = None
        elif width is None:
            self._data = {'type': 'size', 'height': height}
        elif height is None:
            self._data = {'type': 'size', 'width': width}
        else:
            self._data = {'type': 'size', 'width': width, 'height': height}
        return self

    def scale(self, x: int, y: Optional[int] = None) -> 'Geometry':
        self._data = {'type': 'scale', 'x': x, 'y': y}
        return self

    def ratio(self, x: int, y: int) -> 'Geometry':
        self._data = {'type': 'ratio', 'x': x, 'y': y}
        return self

    def area(self, area: int) -> 'Geometry':
        self._data = {'type': 'area', 'area': area}
        return self

    def __str__(self):
        parts = []
        if self._data and self._data['type'] == 'size':
            w = self._data['width'] if 'width' in self._data else ''
            h = self._data['height'] if 'height' in self._data else ''
            parts.append(f"{w}x{h}")
        elif self._data and self._data['type'] == 'scale':
            x = self._data['x']
            y = self._data['y'] if 'y' in self._data else ''
            parts.append(f"{x}%x{y}%")
        elif self._data and self._data['type'] == 'ratio':
            x = self._data['x']
            y = self._data['y']
            parts.append(f"{x}:{y}")
        elif self._data and self._data['type'] == 'area':
            area = self._data['area']
            parts.append(f"{area}@")

        if self._flag:
            parts.append(self._flag)

        if self._offset:
            x = self._offset['x']
            y = self._offset['y']
            parts.append(f"{x:+}{y:+}")

        return ''.join(parts)
class ImageMagickCommandBuilder:
    def __init__(self, resource: Optional[str] = None):
        self._commands = []
        if resource:
            self._commands.append(self._escape(resource))

    def clone(self, index: Optional[Union[int, str]] = None) -> 'ImageMagickCommandBuilder':
        if index is not None:
            self._commands.append('-clone')
            self._commands.append(self._escape(index))
        else:
            self._commands.append('+clone')
        return self

    def parts(self) -> List[str]:
        parts = []
        for part in self._commands:
            if isinstance(part, ImageMagickCommandBuilder):
                parts.extend(part.parts())
            else:
                parts.append(part)
        return parts

    def command(self, *commands: str) -> 'ImageMagickCommandBuilder':
        self._commands.extend(commands)
        return self

    def resource(self, resource: str) -> 'ImageMagickCommandBuilder':
        self._commands.append(self._escape(resource))
        return self

    def parens(self, im: 'ImageMagickCommandBuilder') -> 'ImageMagickCommandBuilder':
        im_parts = im.parts()  # Get the parts of the sub-builder
        self._commands.append('(')
        self._commands.extend(im_parts)
        self._commands.append(')')
        return self

    def composite(self) -> 'ImageMagickCommandBuilder':
        self._commands.append('-composite')
        return self

    def gravity(self, gravity: Optional[str] = None) -> 'ImageMagickCommandBuilder':
        if gravity:
            self._commands.append('-gravity')
            self._commands.append(self._escape(gravity))
        else:
            self._commands.append('+gravity')
        return self

    def geometry(self, x: int, y: int) -> 'ImageMagickCommandBuilder':
        self._commands.append('-geometry')
        self._commands.append(self._escape(Geometry().offset(x, y).__str__()))
        return self

    def size(self, w: Optional[int] = None, h: Optional[int] = None) -> 'ImageMagickCommandBuilder':
        self._commands.append('-size')
        self._commands.append(self._escape(Geometry().size(w, h).__str__()))
        return self

    def extent(self, w: int, h: int) -> 'ImageMagickCommandBuilder':
        self._commands.append('-extent')
        self._commands.append(self._escape(Geometry().size(w, h).__str__()))
        return self

    def resize(self, w: Optional[int] = None,
               h: Optional[int] = None) -> 'ImageMagickCommandBuilder':
        if w or h:
            self._commands.append('-resize')
            self._commands.append(self._escape(Geometry().size(w, h).__str__()))
        return self

    def resizeExt(self, fn: Callable[[Geometry], Geometry]) -> 'ImageMagickCommandBuilder':
        geometry = fn(Geometry())
        self._commands.append('-resize')
        self._commands.append(self._escape(geometry.__str__()))
        return self

    def background(self, background: str) -> 'ImageMagickCommandBuilder':
        self._commands.append('-background')
        self._commands.append(self._escape(background))
        return self

    def trim(self) -> 'ImageMagickCommandBuilder':
        self._commands.append('-trim')
        return self

    def label(self, input: Union[str, int]) -> 'ImageMagickCommandBuilder':
        self._commands.append(f"label:\"{self._escape(input)}\"")
        return self

    def font(self, font: str) -> 'ImageMagickCommandBuilder':
        self._commands.append('-font')
        self._commands.append(self._escape(font))
        return self

    def pointsize(self, size: Optional[int] = None) -> 'ImageMagickCommandBuilder':
        if size:
            self._commands.append('-pointsize')
            self._commands.append(self._escape(size))
        else:
            self._commands.append('+pointsize')
        return self

    def alpha(self, alphaType: str) -> 'ImageMagickCommandBuilder':
        self._commands.append('-alpha')
        self._commands.append(self._escape(alphaType))
        return self

    def interpolate(self, interpolateType: str) -> 'ImageMagickCommandBuilder':
        self._commands.append('-interpolate')
        self._commands.append(self._escape(interpolateType))
        return self

    def filter(self, filterType: str) -> 'ImageMagickCommandBuilder':
        self._commands.append('-filter')
        self._commands.append(self._escape(filterType))
        return self

    def compose(self, composeType: str) -> 'ImageMagickCommandBuilder':
        self._commands.append('-compose')
        self._commands.append(self._escape(composeType))
        return self

    def fill(self, color: str) -> 'ImageMagickCommandBuilder':
        self._commands.append('-fill')
        self._commands.append(self._escape(color))
        return self

    def opaque(self, color: str, invert: Optional[bool] = False) -> 'ImageMagickCommandBuilder':
        if invert:
            self._commands.append('+opaque')
        else:
            self._commands.append('-opaque')
        self._commands.append(self._escape(color))
        return self

    def sanitize(self, input: Union[str, int, float]) -> str:
        return self._escape(input)

    def _escape(self, data: Union[str, int, float]) -> str:
        return str(data)

class Fds:
    def __init__(self):
        self._buffers = []

    def fd(self, buffer: bytes) -> str:
        buffer_start_index = 3
        current_buffer_length = len(self._buffers)

        self._buffers.append(buffer)

        return f'fd:{buffer_start_index + current_buffer_length}'

    def fds(self) -> List[bytes]:
        return self._buffers