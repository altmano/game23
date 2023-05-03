"""
Modul obsahující akce hry.
"""
import dbg

dbg.start_mod(1, __name__)

###########################################################################q

from typing import Callable
from .alto01_altman import *
from . import my_world

def is_alive() -> bool:
    """Vrátí informaci o tom, je-li hra živá = aktuálně spuštěná.
    Spuštěnou hru není možno pustit znovu.
    Chceme-li hru spustit znovu, musíme ji nejprve ukončit.
    """
    return _alive


def execute_command(command: str) -> str:
    """Zpracuje zadaný příkaz a vrátí text zprávy pro uživatele.
    """
    global _alive
    command = command.strip().lower()
    if command: # neprazdny prikaz
        if _alive:
            command_split = command.lower().split()
            action_name = command_split[0]
            if action_name not in command_name_2_action:
                return f"Tento příkaz neznám: {action_name}"

            return command_name_2_action[action_name].execute(command_split[1:])

        else:
            return  WRONG_START.message
    else: # prazdny prikaz
        if _alive:
            return erEMPTY
        _initialize()
        _alive = True
        return  START_STEP.message





def stop() -> None:
    """Ukončí hru a uvolní alokované prostředky.
    Zadáním prázdného příkazu lze následně spustit hru znovu.
    """
    global _alive
    _alive = False


def all_actions() -> 'tuple[IAction]':
    """Vrátí n-tici všech akcí použitelných ve hře.
    """
    return command_name_2_action.values()

############################################################################

def _initialize() -> None:
        """Inicializuje v akcich
        """
        my_world.initialize()



class Action(my_world.ANamed):
    """Společná rodičovská třída všech akcí.
    """

    def __init__(self, name: str, description: str,
                 execute: Callable[[list[str]], str]):
        """Vytvoří instanci, která si zapamatuje
        název dané akce a její popis.
        """
        super().__init__(name=name)
        self._description = description
        self.execute = execute

    @property
    def description(self) -> str:
        """Vrátí popis příkazu s vysvětlením jeho funkce,
        významu jednotlivých parametrů a možností (resp. účelu) použití
        daného příkazu. Tento popis tak může sloužit jako nápověda
        k použití daného příkazu.
        """
        return self._description

    execute: Callable[[list[str]], str] = None
    """Metoda realizující reakci hry na zadání daného příkazu.
    Předávané pole je vždy neprázdné, protože jeho nultý prvek
    je zadaný název vyvolaného příkazu. Počet argumentů je závislý
    na konkrétním akci, ale pro každou akci je konstantní.
    """
_flags: dict[str, object] = dict()
_alive: bool = False



#Akce respektive prikazy hry

# Akce startu hry
def _start_action_execute(_: list[str]) -> str:
    """Zpracuje příkaz startu hry. """
    if is_alive():
        return "Prázdný příkaz lze použít pouze pro start hry"
    _initialize()

    return START_STEP.message


_Start_action = Action(
    name="",
    description="Zapne hru, pokud je vypnutá",
    execute=_start_action_execute
)

# Akce sebrání předmětu
def _take_action_execute(args: list[str]) -> str:
    """Zpracuje příkaz sebrání předmětu."""
    if len(args) == 0:
        return ('Nevím, co mám zvednout.\n'
                'Je třeba zadat název zvedaného objektu.')

    if len(args) > 1:
        return 'Příkaz zvedni má pouze jeden parametr'

    item_name = args[0]
    item = my_world.current_place().item(item_name)
    if item is None:
        return f'Zadaný objekt v prostoru není: {item_name}'

    if not item.movable:
        return f'Zadaný objekt není možno zvednout: {item_name}'

    my_world.BAG.add_item(item)

    #if not my_world.BAG.add_item(item):
        #return f'Zadaný objekt se už do batohu nevejde: {item_name}'

    my_world.current_place().remove_item(item_name)

    return 'Dal sis do batohu ' + item_name


_Take_action = Action(
    name="vezmi",
    description="Zvedne zadaný předmět a vloží jej do batohu.",
    execute=_take_action_execute
)

# Akce přechodu do jiného prostoru
def _move_action_execute(args: list[str]) -> str:
    """Zpracuje příkaz přechodu do jiného prostoru."""
    if len(args) == 0:
        return ('Nevím, kam mám jít.\n'
                'Je třeba zadat název cílového prostoru.')

    if len(args) > 1:
        return 'Příkaz jdi má pouze jeden parametr'

    place_name = args[0]
    place = my_world.current_place().name_2_neighbor(place_name)
    if place is None:
        return f'Do zadaného prostoru se odsud jít nedá: {place_name}'

    my_world.set_current_place(place)
    return 'Přesunul ses do prostoru:\n' + place.description


_Move_action = Action(
    name="jdi",
    description="Přesune hráče do zadaného sousedního prostoru.",
    execute=_move_action_execute
)


#Zbytecny prikaz pokladani ktery definuji jen proto ze musim
def _put_down_action_execute(args: list[str]) -> str:
    """Zpracuje příkaz položení předmětu."""
    if len(args) == 0:
        return ('Nevím, co mám položit.\n'
                'Je třeba zadat název pokládaného objektu.')

    if len(args) > 1:
        return 'Příkaz polož má pouze jeden parametr'

    item_name = args[0]
    item = my_world.BAG.item(item_name)
    if item is None:
        return f'Zadaný objekt v batohu není: {item_name}'

    my_world.current_place().add_item(my_world.BAG.remove_item(item_name))

    return 'Položil jsi předmět: ' + item_name


_Put_down_action = Action(
    name="polož",
    description="Položi predmet z inventare do prostoru",
    execute=_put_down_action_execute
)

# Akce nápovědy
def _help_action_execute(args: list[str]) -> str:
    """Zpracuje příkaz nápovědy."""
    if len(args) > 0:
        return 'Příkaz ? nemá žádné parametry.'

    return SUBJECT


_Help_action = Action(
    name="?",
    description="Zobrazi napovedu ze scenare",
    execute=_help_action_execute
)


# Akce ukončení hry
def _end_action_execute(args: list[str]) -> str:
    """Zpracuje příkaz ukončení hry."""
    if len(args) > 0:
        return 'Příkaz konec nemá žádné parametry.'

    stop()
    return 'Ukončili jste hru.\nDěkujeme, že jste si zahráli.'


_End_action = Action(
    name="konec",
    description="Ukončí hru.",
    execute=_end_action_execute
)


###########################################################################q

# Slovník přiřazující názvy příkazů akcím
command_name_2_action: dict[str, Action] = {
    "": _Start_action,
    "vezmi": _Take_action,
    "jdi": _Move_action,
    "polož": _Put_down_action,
    "?": _Help_action,
    "konec": _End_action,
    #"Kup": _Buy_action,
    #"Uhneť": _Knead_action,
    #"Přidej": _Add_action,
    #"Upeč": _Bake_action,
}

###########################################################################q
dbg.stop_mod(1, __name__)