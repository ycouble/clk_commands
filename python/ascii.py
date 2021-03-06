#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from pathlib import Path

import click

from click_project.decorators import (
    argument,
    flag,
    group,
    option,
    command,
    use_settings,
    table_format,
    table_fields,
)
from click_project.lib import (
    TablePrinter,
    call,
)
from click_project.config import config
from click_project.log import get_logger
from click_project.types import DynamicChoice


LOGGER = get_logger(__name__)

@group()
def ascii():
    """Ascii art commands"""

@ascii.command()
def youpi():
    print(random.choice(HAPPY))

HAPPY = [
    """
                                 .''.
       .''.             *''*    :_\\/_:     . 
      :_\\/_:   .    .:.*_\\/_*   : /\\ :  .'.:.'.
  .''.: /\\ : _\\(/_  ':'* /\\ *  : '..'.  -=:o:=-
 :_\\/_:'.:::. /)\\*''*  .|.* '.\\'/.'_\\(/_'.':'.'
 : /\\ : :::::  '*_\\/_* | |  -= o =- /)\\    '  *
  '..'  ':::'   * /\\ * |'|  .'/.\\'.  '._____
      *        __*..* |  |     :      |.   |' .---"|
       _*   .-'   '-. |  |     .--'|  ||   | _|    |
    .-'|  _.|  |    ||   '-__  |   |  |    ||      |
    |' | |.    |    ||       | |   |  |    ||      |
 ___|  '-'     '    ""       '-'   '-.'    '`      |____
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
""",
    """
                                   .''.
       .''.      .        *''*    :_\\/_:     .
      :_\\/_:   _\\(/_  .:.*_\\/_*   : /\\ :  .'.:.'.
  .''.: /\\ :    /)\\   ':'* /\\ *  : '..'.  -=:o:=-
 :_\\/_:'.:::.  | ' *''*    * '.\\'/.'_\\(/_'.':'.'
 : /\\ : :::::  =  *_\\/_*     -= o =- /)\\    '  *
  '..'  ':::' === * /\\ *     .'/.\\'.  ' ._____
      *        |   *..*         :       |.   |' .---"|
        *      |     _           .--'|  ||   | _|    |
        *      |  .-'|       __  |   |  |    ||      |
     .-----.   |  |' |  ||  |  | |   |  |    ||      |
 ___'       ' /"\\ |  '-."".    '-'   '-.'    '`      |____
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                       ~-~-~-~-~-~-~-~-~-~   /|
          )      ~-~-~-~-~-~-~-~  /|~       /_|\\
        _-H-__  -~-~-~-~-~-~     /_|\\    -~======-~
~-\\XXXXXXXXXX/~     ~-~-~-~     /__|_\\ ~-~-~-~
~-~-~-~-~-~    ~-~~-~-~-~-~    ========  ~-~-~-~
""",
    """
               *    *
   *         '       *       .  *   '     .           * *
                                                               '
       *                *'          *          *        '
   .           *               |               /
               '.         |    |      '       |   '     *
                 \\*        \\   \\             /
       '          \\     '* |    |  *        |*                *  *
            *      `.       \\   |     *     /    *      '
  .                  \\      |   \\          /               *
     *'  *     '      \\      \\   '.       |
        -._            `                  /         *
  ' '      ``._   *                           '          .      '
   *           *\\*          * .   .      *
*  '        *    `-._                       .         _..:='        *
             .  '      *       *    *   .       _.:--'
          *           .     .     *         .-'         *
   .               '             . '   *           *         .
  *       ___.-=--..-._     *                '               '
                                  *       *
                *        _.'  .'       `.        '  *             *
     *              *_.-'   .'            `.               *
                   .'                       `._             *  '
   '       '                        .       .  `.     .
       .                      *                  `
               *        '             '                          .
     .                          *        .           *  *
             *        .                                    '
""",
    """
                                   .''.       
       .''.      .        *''*    :_\\/_:     . 
      :_\\/_:   _\\(/_  .:.*_\\/_*   : /\\ :  .'.:.'.
  .''.: /\\ :   ./)\\   ':'* /\\ * :  '..'.  -=:o:=-
 :_\\/_:'.:::.    ' *''*    * '.\\'/.' _\\(/_'.':'.'
 : /\\ : :::::     *_\\/_*     -= o =-  /)\\    '  *
  '..'  ':::'     * /\\ *     .'/.\\'.   '
      *            *..*         :
       *
        *
""",
    """
         .* *.               `o`o`
         *. .*              o`o`o`o      ^,^,^
           * \\               `o`o`     ^,^,^,^,^
              \\     ***        |       ^,^,^,^,^
               \\   *****       |        /^,^,^
                \\   ***        |       /
    ~@~*~@~      \\   \\         |      /
  ~*~@~*~@~*~     \\   \\        |     /
  ~*~@smd@~*~      \\   \\       |    /     #$#$#        .`'.;.
  ~*~@~*~@~*~       \\   \\      |   /     #$#$#$#   00  .`,.',
    ~@~*~@~ \\        \\   \\     |  /      /#$#$#   /|||  `.,'
_____________\\________\\___\\____|_/______/_________|\\/\\___||______
"""
]
