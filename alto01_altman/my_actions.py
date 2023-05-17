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

            return command_name_2_action[action_name].\
                execute(command_split[1:])

        else:
            return  WRONG_START.message
    else: # prazdny prikaz
        if _alive:
            return erEMPTY
        _initialize()
        _alive = True
        return  START_STEP.message

def tests() -> dict[str, object]:
    """Vrátí slovník jehož hodnotami jsou testovací funkce
    ověřující platnost vstupních podmínek pomocných akcí.
    """
    return _TESTNAMES_TO_TESTS

def conditions() -> dict[str, object]:
    """Vrátí slovník s aktuálním nastavením příznaků.
    """
    return _flags



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
        global _flags, _alive
        _flags['Peněženka.balance'] = 300
        _flags['Těsto.toppingcount'] = 0
        _flags['uhneteno' ] = False
        _alive = True


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

_flags: dict[str, object] = START_STEP.sets
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
        return f'Zadaný objekt v BAG není: {item_name}'

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

def _buy_action_execute(args: list[str]) -> str:
    """Zpracuje příkaz ukončení hry."""
    if len(args) == 0:
        return 'Nevím, co mám koupit'

    if len(args) > 1:
        return 'Příkaz kup má pouze jeden parametr'

    if my_world.current_place().name.lower() == 'byt'\
        or my_world.current_place().name.lower() == 'ulice'\
        or my_world.current_place().name.lower() == 'obchod_s_potravinami' :
        return 'Nelze koupit objekt ' + args[0]

    item_name = args[0]
    item = my_world.current_place().item(item_name)
    if item is None:
        return f'Zadaný objekt v prostoru není: {item_name}'

    if item.movable:
        return f'Zadaný předmět nelze koupit: {item_name}'

    penezenka = my_world.BAG.item('Peněženka')
    if  penezenka is None:
        return 'Nemuzes kupovat, nemáš peněženka'

    trytobuy = my_world.BAG.add_item(item)

    if trytobuy:
        _set_flag(penezenka,'balance', my_world.BAG.capacity)
        return 'Dal sis do batohu ' + item_name
    else:
        return 'Nelze koupit předmět, na který nemáš: ' + item_name



_Buy_action = Action(
    name="kup",
    description="Zkusí koupit zadaný předmět.",
    execute=_buy_action_execute
)


def _knead_action_execute(args: list[str]) -> str:
    """Zpracuje příkaz uhnetení těsta"""
    if len(args) > 0:
        return 'Příkaz uhneť nemá žádné parametry.'

    if my_world.current_place().name.lower() != 'byt':
        return 'Tady nelze hnist. Musis byt v byt'

    if _flags['uhneteno']:
        return 'Uz mas hotove testo, nepotrebujes znovu Uhněť'

    mouka = my_world.BAG.item('mouka')
    olej = my_world.BAG.item('olivovy_olej')
    drozdi = my_world.BAG.item('droždí')
    voda = my_world.BAG.item('voda')
    sul = my_world.BAG.item('sůl')

    if mouka is None or olej is None or drozdi is None :
        return 'Nekoupil jsi mouku, olej nebo drozdi, nemuzes uhneť'
    if voda is None or sul is None:
        return 'Vezmi vodu a sul, ktere potrebujes na uhneť'

    my_world.BAG.remove_item('mouka')
    my_world.BAG.remove_item('olivovy_olej')
    my_world.BAG.remove_item('droždí')
    my_world.BAG.remove_item('voda')
    my_world.BAG.remove_item('sůl')

    my_world.BAG.add_item(my_world.Item('Těsto', True, 0))
    _flags['uhneteno'] = True
    return 'Použil jsi vodu, sůl, mouku, droždí a olivový olej na unětění těsto'


_Knead_action = Action(
    name="uhneť",
    description="Uhněte z dostupných surovin těsto na pizzu.",
    execute=_knead_action_execute
)

def _add_action_execute(args: list[str]) -> str:
    """Zpracuje příkaz ukončení hry."""
    if len(args) == 0:
        return 'Nevím co mám Přidej'
    if len(args) > 1:
        return 'Příkaz Přidej má pouze jeden parametr'

    testo = my_world.BAG.item('těsto')
    if testo is None:
        return 'Neni uhnetene testo, nelze Přidej'

    item_name = args[0]
    if item_name == 'peněženka' or item_name == 'klíče':
        return 'Na pizzu nelze přidata objekt: ' + item_name

    item = my_world.BAG.item(item_name)
    if item is None:
        return 'Nelze přidat nepřítomný objekt: ' + item_name

    my_world.BAG.add_topping(item_name)
    _set_flag(testo, 'toppingcount', my_world.BAG.topping_count)
    return 'Na těsto bylo přidáno: ' + item_name




_Add_action = Action(
    name="přidej",
    description="Přidá topping na připravené těsto.",
    execute=_add_action_execute
)

def _bake_action_execute(args: list[str]) -> str:
    """Zpracuje příkaz ukončení hry."""
    if len(args) != 0:
        return 'Příkaz nemá žádné parametry'


    testo = my_world.BAG.item('těsto')
    if testo is None or my_world.BAG.topping_count < 2:
        return 'Nemáš připravenou pizzu k Upeč'

    if my_world.current_place().name.lower() != 'byt':
        return 'Musíš být v byt. Tady nejde Upeč'
    my_world.BAG.remove_item('těsto')
    #my_world.BAG.add_item(my_world.Item('Těsto', True, 0))
    my_world.BAG.add_item(my_world.Item('Pizza', True, 0))
    #_flags.clear()
    for key in _flags:
        _flags[key] = START_STEP.sets[key]

    stop()
    return 'Vložil jsi použitelnou verzi pizzy do trouby\n'\
        + 'Úspěšně jste ukončili hru.\nDěkujeme, že jste si zahráli.'






_Bake_action = Action(
    name="upeč",
    description="Upeče připravenou pizzu a ukončí hru",
    execute=_bake_action_execute
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
    "kup": _Buy_action,
    "uhneť": _Knead_action,
    "přidej": _Add_action,
    "upeč": _Bake_action,
}

def _argument_present(arguments:tuple[str]) -> bool:
    """
    Zjišťuje, zda je argument aktuálního příkazu
    názvem h-objektu přítomného v aktuálním prostoru.
    :param arguments: Zpracovávaný příkaz rozdělený na slova
    :return: Logická hodnota indikující splnění testované podmínky
    """
    return _get_argument(arguments)

def _argument_buyable(arguments:tuple[str]) -> bool:
    """
    Zjišťuje, zda je argument aktuálního příkazu
    názvem h-objektu přítomného v aktuálním prostoru a jestli
    ho lze koupit.
    :param arguments: Zpracovávaný příkaz rozdělený na slova
    :return: Logická hodnota indikující splnění testované podmínky
    """
    item = _get_argument(arguments)
    if item.movable:
        return False
    return True

def _ingredients_present(_: tuple[str, ...]) -> bool:
    """
    Zjišťuje, zda je argument aktuálního příkazu
    názvem h-objektu přítomného v aktuálním prostoru a jestli
    ho lze koupit.
    :return: Logická hodnota indikující splnění testované podmínky
    """
    mouka = my_world.BAG.item('mouka')
    olej = my_world.BAG.item('olivovy_olej')
    drozdi = my_world.BAG.item('droždí')
    voda = my_world.BAG.item('voda')
    sul = my_world.BAG.item('sůl')



    if mouka is not None and olej is not None and drozdi is not None and\
        voda is not None and sul is not None:
        return True
    return False


def _dough_present(_: tuple[str, ...]) -> bool:
    """
    Zjišťuje, zda je argument aktuálního příkazu
    názvem h-objektu přítomného v aktuálním prostoru a jestli
    ho lze koupit.
    :return: Logická hodnota indikující splnění testované podmínky
    """
    testo = my_world.BAG.item('těsto')

    if testo is not None:
        return True
    return False

def _vprostoru_lzeKoupit(_: tuple[str, ...]) -> bool:
    """
    Zjišťuje, zda je argument aktuálního příkazu
    názvem h-objektu přítomného v aktuálním prostoru a jestli
    ho lze koupit.
    :return: Logická hodnota indikující splnění testované podmínky
    """
    current_place = my_world.current_place()

    if current_place.name.lower() == 'regaly' or\
        current_place.name.lower() == 'oddělení_chlazenych':
        return True
    return False

def _get_argument(arguments:tuple[str, ...]) -> 'Item':
    """
    Ověří, je-li v aktuálním prostoru objekt se zadaným názvem,
    a pokud ano, vrátí odkaz na něj. Jinak vrátí None.
    :param arguments: Zpracovávaný příkaz rozdělený na slova
    :return: Požadovaný odkaz či None
    """
    lower_name = arguments[1].lower()
    current_place = my_world.current_place()
    item = current_place.item(lower_name)
    return item

def _get_flag(item:'Item', flagname:str) -> object:
    """
    Složí název zjišťovaného příznaku z názvu h-objektu a označení příznaku,
    a vrátí hodnotu takto pojmenovaného příznaku.
    :param item:     H-objekt, na jehož vlastnost se ptátme
    :param flagname: Označení zjišťované charakteristiky
    :return: Požadovaná hodnota
    """
    full_name = item.name + '.' + flagname
    result    = _flags[full_name]
    return result


def _set_flag(item:'Item', flagname:str, value:object) -> None:
    """
    Složí název zjišťovaného příznaku z názvu h-objektu a označení příznaku,
    a nastaví hodnotu takto pojmenovaného příznaku.
    :param item:     H-objekt, jehož vlastnost nastavujeme
    :param flagname: Označení zjišťované charakteristiky
    :param value: Nastavovaná hodnota
    :return:
    """
    full_name = item.name + '.' + flagname
    _flags[full_name] = value


_TESTNAMES_TO_TESTS: dict[str, Callable[[tuple[str, ...]], bool]] = dict(
    argument_present =_argument_present,   # Argument je v aktuálním prostoru
    argument_buyable=_argument_buyable,  # Argument je buditelný
    ingredients_present=_ingredients_present, # Ma ingredience na testo
    dough_present=_dough_present,# Ma uhnetene testo
    vprostoru_lzeKoupit=_vprostoru_lzeKoupit, # V akt. prost. lze koupit
)

###########################################################################q
dbg.stop_mod(1, __name__)