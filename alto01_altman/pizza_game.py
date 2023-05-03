"""
Modul obsahující základ hry.
"""
import dbg

dbg.start_mod(1, __name__)

###########################################################################q

from game23s.api import BasicActions
from game23s.api.interfaces import *
from game23s.api.interfaces import IAction, IBag, IWorld

from . import  my_actions
from . import  my_world


def is_alive() -> bool:
    """Vrátí informaci o tom, je-li hra aktuálně spuštěná.
    Spuštěnou hru není možno pustit znovu.
    Chceme-li hru spustit znovu, musíme ji nejprve ukončit.
    """

    return my_actions.is_alive()

def execute_command(command :str) -> str:
    """Zpracuje zadaný příkaz a vrátí text zprávy pro uživatele.
    """

    return my_actions.execute_command(command)



def stop() -> None:
    """Ukončí hru a uvolní alokované prostředky.
    Zadáním prázdného příkazu lze následně spustit hru znovu.
    """
    my_actions.stop()



def all_actions() -> tuple[IAction]:
    """Vrátí n-tici všech akcí použitelných ve hře.
    """
    return tuple(my_actions.command_name_2_action.values())[1:]


def basic_actions() -> BasicActions:
    """Vrátí přepravku s názvy povinných akcí.
    """
    return BasicActions(
        MOVE_NAME='Jdi',
        PUT_DOWN_NAME= 'Polož',
        TAKE_NAME= 'Vezmi',
        HELP_NAME= '?',
        END_NAME='KONEC',
        SUCCESS_NAME='Upeč'
    )



def bag() -> IBag:
    """Vrátí odkaz na batoh, do nějž bude hráč ukládat sebrané objekty.
    """
    from .my_world import BAG
    return BAG


def world() -> IWorld:
    """Vrátí odkaz na svět hry.
    """
    return my_world


def conditions() -> dict[str, object]:
    """Vrátí slovník s aktuálním nastavením příznaků.
    """
    from .alto01_altman import START_STEP
    return  START_STEP.sets

def tests() -> dict[str, object]:
    """Vrátí slovník jehož hodnotami jsou testovací funkce
        ověřující platnost vstupních podmínek pomocných akcí.
        """
    raise {}


###########################################################################q
dbg.stop_mod(1, __name__)