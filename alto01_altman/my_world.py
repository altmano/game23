"""
Modul obsahující svět hry.
"""
from tkinter import Place

import dbg

dbg.start_mod(1, __name__)

from .alto01_altman import *

############################################################################



class ANamed():
    """Instance představují objekty v prostorech či batohu.
    """

    def __init__(self, name:str, **args):
        """Inicializuje objekt zadaným názvem.
        """
        super().__init__(**args)
        #raise Exception(f'Ještě není plně implementováno')
        self._name = name


    @property
    def name(self) -> str:
        """Vrátí název daného objektu.
        """
        #raise Exception(f'Ještě není plně implementováno')
        return self._name


    def __str__(self) -> str:
        """Vrátí uživatelský textový podpis jako název dané instance.
        """
        return self.name
        #raise Exception(f'Ještě není plně implementováno')



############################################################################

 
class Item(ANamed):
    """Instance představují h-objekty v prostorech či batohu.
    """

    def __init__(self,
                 name:str,
                 movable: bool,
                 weight: int,
                 **args):
        """Vytvoří h-objekt se zadaným názvem.
        """
        self._movable = movable
        self._weight = weight
        super().__init__(name=name, **args)

    @property
    def weight(self) -> int:
        """Vrátí váhu daného objektu.
        """
        return self._weight
        #raise Exception(f'Ještě není plně implementováno')

    @property
    def movable(self) -> bool:
        """Vrátí informaci o tom, je-li objekt přenositelný.
        """
        return self._movable

    def __repr__(self):
        """Vrátí textový podpis dané instance.
        """
        return f"{self.__class__.__name__}({self.name})"

############################################################################

 
class AItemContainer:
    """Instance představují kontejnery objektů - prostory či batoh.
    V kontejneru může být několik objektů se shodným názvem.
    """

    def __init__(self, initial_item_names: tuple[str], **args):
        """Zapamatuje si názvy výchozí sady objektů na počátku hry.
        """

        self.initial_item_names = initial_item_names
        super().__init__(**args)
        self._items = []
        self._item_names = []

    def initialize(self) -> None:
        """Inicializuje kontejner na počátku hry.
        Po inicializace bude obsahovat příslušnou výchozí sadu objektů.
        Protože se názvy objektů mohou opakovat, nemůže použít slovník.
        Pamatuje si proto seznam objektů a seznam jejích názvů malými písmeny.
        Musí se jen dbát na to, aby se v obou seznamech vyskytoval objekt
        a jeho název na pozicích se stejným indexem.
        """
        from . import my_actions

        self._items = []
        self._item_names = []
        for item_name in self.initial_item_names:
            item = Item(
                name=item_name,
                movable= True,
                weight= 1,
            )
            if item.name.lower() not in self._item_names:
                self._items.append(item)
                self._item_names.append(item_name.lower())



    @property
    def items(self) -> list[Item]:
        """Vrátí n-tici objektů v daném kontejneru.
        """
        return self._items[:]


    def item(self, name:str) -> Item:
        """Je-li v kontejneru objekt se zadaným názvem, vrátí jej,
        jinak vrátí None.
        """
        name_lower = name.lower()
        if name_lower in self._item_names:
            return self._items[self._item_names.index(name_lower)]
        return None




    def add_item(self, item:Item) -> bool:
        """Přidá zadaný objekt do kontejneru a vrátí informaci o tom,
        jestli se to podařilo.
        """
        name_lower = item.name.lower()
        if name_lower not in self._item_names:
            self._item_names.append(name_lower)
            self._items.append(item)
            return True
        else:
            return False


    def remove_item(self, item_name:str) -> Item:
        """Pokusí se odebrat objekt se zadaným názvem z kontejneru.
        Vrátí odkaz na zadaný objekt nebo None.
        """
        name = item_name.lower()
        for i, n in enumerate(self._item_names):
            if name == n:
                result = self._items[i]
                del self._items[i]
                del self._item_names[i]
                return result

        return None



############################################################################

 
class Bag(AItemContainer):
    """Instance představuje úložiště,
    do nějž hráči ukládají objekty sebrané v jednotlivých prostorech,
    aby je mohli přenést do jiných prostorů a/nebo použít.
    Úložiště má konečnou kapacitu definující maximální povolený
    součet vah objektů vyskytujících se v úložišti.
    """

    def __init__(self, initial_item_names: tuple[str] | tuple, **args):
        """Definuje batoh jako kontejner h-objektů s omezenou kapacitou.
          """
        global BAG
        if BAG:
            raise Exception(f'Více než jeden batoh')
        self._capacity = 0
        super().__init__(initial_item_names, **args)
        BAG = self


    def initialize(self) -> None:
        """Inicializuje batoh na počátku hry. Vedle inicializace obsahu
        inicializuje i informaci o zbývající kapacitě.
        """
        self._capacity = 0
        self._items = []
        self._item_names = []
        super().initialize()


    @property
    def capacity(self) -> int:
        """Vrátí kapacitu batohu.
        """
        return self._capacity

    def add_item(self, item: Item) -> bool:
        """Přidá zadaný objekt do batohu a vrátí informaci o tom,
        jestli se to podařilo.
        """
        if item.weight + self._capacity <= 50:
            self._capacity += item.weight
            return super().add_item(item)
        return False

    def remove_item(self, item_name: str) -> Item:
        """Pokusí se odebrat objekt se zadaným názvem z batohu.
        Vrátí odkaz na zadaný objekt nebo None.
        """
        item = super().remove_item(item_name)
        if item:
            self._capacity -= item.weight
        return item



############################################################################

 
class Place(ANamed, AItemContainer):
    """Instance představují prostory, mezi nimiž hráč přechází.
    Prostory jsou definovány jako pojmenované kontejnery objektů.
    Prostory mohou obsahovat různé objekty,
    které mohou hráči pomoci v dosažení cíle hry.
    Každý prostor zná své aktuální bezprostřední sousedy
    a ví, jaké objekty se v něm v daném okamžiku nacházejí.
    Sousedé daného prostoru i v něm se nacházející objekty
    se mohou v průběhu hry měnit.
    """

    def __init__(self, name: str, description: str,
                 initial_neighbor_names: tuple[str, ...],
                 initial_item_names: tuple[str, ...], **args
                 ):
        super().__init__(name=name, initial_item_names=initial_item_names,
                         **args)
        self._neighbors = {}
        self._description = description
        self._initial_neighbor_names = initial_neighbor_names


    def initialize(self) -> None:
        """Inicializuje prostor na počátku hry,
        tj. nastaví počáteční sadu sousedů a objektů v prostoru.
        """
        super().initialize()
        #self._neighbor = {}
        for n in self._initial_neighbor_names:
            n = n.lower()
            self._neighbors[n] = _NAME_2_PLACE[n]

        super().initialize()


    @property
    def description(self) -> str:
        """Vrátí stručný popis daného prostoru.
        """
        return self._description


    @property
    def neighbors(self) -> tuple['Place'] | tuple:
        """Vrátí n-tici aktuálních sousedů daného prostoru,
        tj. prostorů, do nichž je možno se z tohoto prostoru přesunout
        příkazem typu `TypeOfStep.GOTO`.
        """
        return tuple(self._neighbors.values())

    def name_2_neighbor(self, name: str) -> 'Place':
        """Vrátí odkaz na souseda se zadaným názvem.
        Není-li takový, vrátí `None`.
        """
        return self._neighbors.get(name.lower())



############################################################################

 

def initialize() -> None:
    """Inicializuje svět hry, tj. nastavuje vzájemné počáteční
    propojení jednotlivých prostorů a jejich výchozí obsah,
    nastaví výchozí aktuální prostor a inicializuje batoh.
    """
    global _current_place
    for place in _PLACES:
        place.initialize()
    _current_place = _NAME_2_PLACE['byt']
    BAG.initialize()

def set_current_place(p: Place) -> None:
    """Nastaví aktuální prostor.
        """
    global _current_place
    _current_place = p

def current_place() -> Place:
    """Vrátí odkaz na aktuální prostor,
    tj. na prostor, v němž se hráč pravé nachází.
    """
    return _current_place


def places() -> tuple[Place]:
    """Vrátí n-tici odkazů na všechny prostory ve hře
    včetně těch aktuálně nedosažitelných či neaktivních.
    """
    return tuple(_NAME_2_PLACE.values())


def place(name:str) -> Place:
    """Vrátí prostor se zadaným názvem.
    Pokud ve hře takový není, vrátí None.
    """
    if name not in _PLACES:
        return None
    return _NAME_2_PLACE[name]


###########################################################################q

BAG: Bag | None = None
BAG = Bag(())
_current_place: Place | None = None



_PLACES = (
     Place('Byt', 'Byt kde lze upect pizzu',
        ('Ulice',),
        ('Peněženka', 'Klíče', 'Sůl', 'Voda',),
        ),
        Place('Ulice', dLES,
              ('Byt', 'Obchod_s_potravinami', ),  # Aktuální sousedé
              (),
              ),
        Place('Obchod_s_potravinami', dOBCHOD,
             ('Ulice', 'Oddělení_chlazenych', 'Regaly',),
             # Aktuální sousedé
             (),
             ),
        Place('Regaly', dREGALY,
               ('Oddělení_chlazenych', 'Obchod_s_potravinami',),
               # Aktuální sousedé
               ('Mouka', 'Cukr', 'Droždí', 'Olivovy_olej',
                'Rajčatová_pasta', 'Česknek', 'Olivy',
                'Cibule', 'Kukuřice', 'Bazalka', 'Ananas',),
               ),
        Place('Oddělení_chlazenych', dCHLADAK,
            ('Regaly', 'Obchod_s_potravinami',),
            # Aktuální sousedé
            ('Šunka', 'Salám', 'Mozzarela',),
            # H-objekty v prostoru
            ),
)

_NAME_2_PLACE = {p.name.lower(): p for p in _PLACES}

NAME_2_PLACE = dict(
    byt = Place('Byt', 'Byt kde lze upect pizzu',
                ('Ulice',),
                ('Peněženka', 'Klíče', 'Sůl', 'Voda',)
                ),
    ulice = Place('Ulice', dLES,
                  ('Byt', 'Obchod_s_potravinami',),  # Aktuální sousedé
                  (),
                  ),
    Obchod_s_potravinami = Place('Obchod_s_potravinami', dOBCHOD,
                  ('Ulice', 'Oddělení_chlazenych', 'Regaly'),
                  (),
                  ),
    Regaly = Place('Regaly', dREGALY,
                  ('Oddělení_chlazenych', 'Obchod_s_potravinami',),
                   ('Mouka', 'Cukr', 'Droždí', 'Olivovy_olej',
                    'Rajčatová_pasta', 'Česknek', 'Olivy',
                    'Cibule', 'Kukuřice', 'Bazalka', 'Ananas',),
                  ),
    Oddělení_chlazenych = Place('Oddělení_chlazenych', dCHLADAK,
                    ('Regaly', 'Obchod_s_potravinami',),  # Aktuální sousedé
                   ('Šunka', 'Salám', 'Mozzarela',),  # H-objekty v prostoru
                  ),
)




###########################################################################q
dbg.stop_mod(1, __name__)