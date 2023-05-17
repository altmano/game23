#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
#V:/p1_GAME_23s_PRJ/GAME_23s/a1b_all/ck_scenarios.py
"""
Základní čtveřice scénářů pro hru inspirovanou
tím, že jsem zrovna den před vymýšlením HAPPY scénáře dělal k večeři pizzu.
Kroky jsou doplněny o podmínky k jejich úspěšnému provedení.
"""
import dbg; dbg.start_mod(1, __name__)
###########################################################################q

from game23s.api.scenario   import ScenarioStep, Scenario
from game23s.api.scen_types import *  # Především typu kroků



###########################################################################q
ScenarioStep.next_index = 0   # Index prvního kroku za startem

place_details = {

}

SUBJECT = (
    'Vaším cílem v této hře je upéct si doma pizzu.\n'
    'Přišli jste večer po práci domů a máte chuť na domácí pizzu \n'
    'doma však nemáte potřebné suroviny.\n'
    'Musíte si tedy dojít do obchodu, který ale za čtvrt hodiny zavírá,\n'
    'takže budete mít pouze jednu šanci. Když něco důležitého\n'
    'zapomenete, tak budete o hladu. V peněžence máte pouze 300 kč, \n'
    'takže nesmíte utratit příliš mnoho peněz topping.\n\n'
    )

# Základní úspěšný scénář demonstrující průběh hry, při němž hráč
# nezadává žádné chybné příkazy a dosáhne zadaného cíle.
HAPPY = Scenario(stHAPPY, (
    START_STEP :=
    ScenarioStep(tsSTART, '',                       # Zadaný příkaz
        WELCOME := 'Vítejte!\n' + SUBJECT
      + '\nNebudete-li si vědět rady, zadejte znak ?, jenž zobrazí nápovědu.',
         'Byt',  # Aktuální prostor
         ('Ulice',),  # Aktuální sousedé
         ('Peněženka', 'Klíče', 'Sůl', 'Voda',),  # H-objekty v prostoru
         (),  # H-Objekty v batohu

        # Počáteční stavy stavových proměnných
        sets ={ 'Peněženka.balance' : 300,
                'Těsto.toppingcount' : 0,


                'uhneteno' : False,
                'balance' : ('Peněženka'), # Objekty, které obsahuji penize
                'cost'    : ('Mouka', 'Cukr', 'Droždí', 'Olivovy_olej',
                'Rajčatová_pasta', 'Česknek', 'Olivy',
                'Cibule', 'Kukuřice', 'Bazalka', 'Ananas',
                'Šunka', 'Salám', 'Mozzarela',), # Objekty, které stoji penize
                },
        tests = ['argument_present',   # Argument je v aktuálním prostoru
                 'argument_buyable',  # Argument je buditelný
                 'ingredients_present' # Ma ingredience na Těsto
                 'dough_present' # Ma uhnetene Těsto
                 'vprostoru_lzeKoupit', # V akt. prost. lze koupit
                  ], # V ak. p. je již pozdravený objekt
    ),
    ScenarioStep(tsTAKE, 'Vezmi Klíče',  # Zadaný příkaz
             'Dal sis do batohu klíče',
             'Byt',  # Aktuální prostor
             ('Ulice',),  # Aktuální sousedé
             ('Peněženka', 'Sůl', 'Voda',),  # H-objekty v prostoru
             ('Klíče',),  # H-Objekty v batohu
             ),
    ScenarioStep(tsTAKE, 'Vezmi Peněženka',  # Zadaný příkaz
             'Dal sis do batohu Peněženka',
             'Byt',  # Aktuální prostor
             ('Ulice',),  # Aktuální sousedé
             ('Sůl', 'Voda',),  # H-objekty v prostoru
             ('Klíče', 'Peněženka',),  # H-Objekty v batohu
             ),
    ScenarioStep(tsGOTO, 'Jdi Ulice',  # Zadaný příkaz
             'Přesunul ses do prostoru:\n'
             + (dLES := 'Ulice s lidmy, obchody a domy'),
             'Ulice',  # Aktuální prostor
             ('Byt', 'Obchod_s_potravinami',),  # Aktuální sousedé
             (),  # H-objekty v prostoru
             ('Klíče', 'Peněženka',),  # H-Objekty v batohu
             ),
    ScenarioStep(tsGOTO, 'Jdi Obchod_s_potravinami',  # Zadaný příkaz
             'Přesunul ses do prostoru:\n'
             + (dOBCHOD := 'Obchod se spoustou potravin'),
             'Obchod_s_potravinami',  # Aktuální prostor
             ('Ulice', 'Oddělení_chlazenych', 'Regaly'),  # Aktuální sousedé
             (),  # H-objekty v prostoru
             ('Klíče', 'Peněženka',),  # H-Objekty v batohu
             ),
    ScenarioStep(tsGOTO, 'Jdi Regaly',  # Zadaný příkaz
             'Přesunul ses do prostoru:\n'
            + (dREGALY := 'Regaly s jidlem ktere nepotrebuje chladit'),
             'Regaly',  # Aktuální prostor
             ('Oddělení_chlazenych', 'Obchod_s_potravinami',),
             # Aktuální sousedé
             ('Mouka', 'Cukr', 'Droždí', 'Olivovy_olej',
              'Rajčatová_pasta', 'Česknek', 'Olivy',
              'Cibule', 'Kukuřice', 'Bazalka', 'Ananas',),
             # H-objekty v prostoru
             ('Klíče', 'Peněženka',),  # H-Objekty v batohu
             ),
    ScenarioStep(tsNS_1, 'Kup mouka',  # Zadaný příkaz
             'Dal sis do batohu mouka',
             'Regaly',  # Aktuální prostor
             ('Oddělení_chlazenych', 'Obchod_s_potravinami',),
             # Aktuální sousedé
             ('Mouka', 'Cukr', 'Droždí', 'Olivovy_olej',
              'Rajčatová_pasta', 'Česknek', 'Olivy',
              'Cibule', 'Kukuřice', 'Bazalka', 'Ananas',),
             # H-objekty v prostoru
             ('Klíče', 'Peněženka', 'Mouka',),  # H-Objekty v batohu

             needs={'Peněženka.balance' : 300, },
             tests=['argument_buyable', 'argument_present',
                    'vprostoru_lzeKoupit', ],
             sets={'Peněženka.balance': 275,},
             ),
    ScenarioStep(tsNS_1, 'Kup Olivovy_olej',  # Zadaný příkaz
             'Dal sis do batohu Olivovy_olej',
             'Regaly',  # Aktuální prostor
             ('Oddělení_chlazenych', 'Obchod_s_potravinami',),
             # Aktuální sousedé
             ('Mouka', 'Cukr', 'Droždí', 'Olivovy_olej',
              'Rajčatová_pasta', 'Česknek', 'Olivy',
              'Cibule', 'Kukuřice', 'Bazalka', 'Ananas',),
             # H-objekty v prostoru
             ('Klíče', 'Peněženka', 'Mouka', 'Olivovy_olej'),
             # H-Objekty v batohu
                 needs={'Peněženka.balance': 275, },
                 tests=['argument_buyable', 'argument_present',
                        'vprostoru_lzeKoupit', ],
                 sets={'Peněženka.balance': 155,},
             ),
    ScenarioStep(tsNS_1, 'Kup Rajčatová_pasta',  # Zadaný příkaz
             'Dal sis do batohu Rajčatová_pasta',
             'Regaly',  # Aktuální prostor
             ('Oddělení_chlazenych', 'Obchod_s_potravinami',),
             # Aktuální sousedé
             ('Mouka', 'Cukr', 'Droždí', 'Olivovy_olej',
              'Rajčatová_pasta', 'Česknek', 'Olivy',
              'Cibule', 'Kukuřice', 'Bazalka', 'Ananas',),
             # H-objekty v prostoru
             ('Klíče', 'Peněženka', 'Mouka', 'Olivovy_olej',
              'Rajčatová_pasta',),  # H-Objekty v batohu
                 needs={'Peněženka.balance': 155, },
                 tests=['argument_buyable', 'argument_present',
                        'vprostoru_lzeKoupit', ],
                 sets={'Peněženka.balance': 115,},
             ),
    ScenarioStep(tsNS_1, 'Kup Droždí',  # Zadaný příkaz
             'Dal sis do batohu Droždí',
             'Regaly',  # Aktuální prostor
             ('Oddělení_chlazenych', 'Obchod_s_potravinami',),
             # Aktuální sousedé
             ('Mouka', 'Cukr', 'Droždí', 'Olivovy_olej',
              'Rajčatová_pasta', 'Česknek', 'Olivy',
              'Cibule', 'Kukuřice', 'Bazalka', 'Ananas',),
             # H-objekty v prostoru
             ('Klíče', 'Peněženka', 'Mouka', 'Olivovy_olej',
              'Rajčatová_pasta', 'Droždí'),  # H-Objekty v batohu
                 needs={'Peněženka.balance': 115, },
                 tests=['argument_buyable', 'argument_present',
                        'vprostoru_lzeKoupit', ],
                 sets={'Peněženka.balance': 105,},
             ),
    ScenarioStep(tsGOTO, 'Jdi Oddělení_chlazenych',  # Zadaný příkaz
             'Přesunul ses do prostoru:\n'
             + (dCHLADAK := 'Chladici boxy s jidlem co musi byt studene'),
             'Oddělení_chlazenych',  # Aktuální prostor
             ('Regaly', 'Obchod_s_potravinami'),
             # Aktuální sousedé
             ('Šunka', 'Salám', 'Mozzarela',),  # H-objekty v prostoru
             ('Klíče', 'Peněženka', 'Mouka', 'Olivovy_olej',
              'Rajčatová_pasta', 'Droždí'),  # H-Objekty v batohu
             ),
    ScenarioStep(tsNS_1, 'Kup Mozzarela',  # Zadaný příkaz
             'Dal sis do batohu Mozzarela',
             'Oddělení_chlazenych',  # Aktuální prostor
             ('Regaly', 'Obchod_s_potravinami'),  # Aktuální sousedé
             ('Šunka', 'Salám', 'Mozzarela',),  # H-objekty v prostoru
             ('Klíče', 'Peněženka', 'Mouka', 'Olivovy_olej',
              'Rajčatová_pasta', 'Droždí', 'Mozzarela',),  # H-Objekty v batohu
                 needs={'Peněženka.balance': 105, },
                 tests=['argument_buyable', 'argument_present',
                        'vprostoru_lzeKoupit', ],
                 sets={'Peněženka.balance': 80,},
             ),
    ScenarioStep(tsGOTO, 'Jdi Obchod_s_potravinami',  # Zadaný příkaz
             'Přesunul ses do prostoru:\n'
             + (dOBCHOD),
             'Obchod_s_potravinami',  # Aktuální prostor
             ('Ulice', 'Oddělení_chlazenych', 'Regaly'),  # Aktuální sousedé
             (),  # H-objekty v prostoru
             ('Klíče', 'Peněženka', 'Mouka', 'Olivovy_olej',
              'Rajčatová_pasta', 'Droždí', 'Mozzarela',),  # H-Objekty v batohu
             ),
    ScenarioStep(tsGOTO, 'Jdi Ulice',  # Zadaný příkaz
             'Přesunul ses do prostoru:\n'
             + (dLES),
             'Ulice',  # Aktuální prostor
             ('Byt', 'Obchod_s_potravinami',),  # Aktuální sousedé
             (),  # H-objekty v prostoru
             ('Klíče', 'Peněženka', 'Mouka', 'Olivovy_olej',
              'Rajčatová_pasta', 'Droždí', 'Mozzarela',),  # H-Objekty v batohu
             ),
    ScenarioStep(tsGOTO, 'Jdi Byt',  # Zadaný příkaz
             'Přesunul ses do prostoru:\n'
             +'Byt kde lze upect pizzu',
             'Byt',  # Aktuální prostor
             ('Ulice',),  # Aktuální sousedé
             ('Sůl', 'Voda',),  # H-objekty v prostoru
             ('Klíče', 'Peněženka', 'Mouka', 'Olivovy_olej',
              'Rajčatová_pasta', 'Droždí', 'Mozzarela',),  # H-Objekty v batohu
             ),
    ScenarioStep(tsPUT_DOWN, 'Polož Klíče',  # Zadaný příkaz
             'Položil jsi předmět: klíče',
             'Byt',  # Aktuální prostor
             ('Ulice',),  # Aktuální sousedé
             ('Sůl', 'Voda', 'Klíče',),  # H-objekty v prostoru
             ('Peněženka', 'Mouka', 'Olivovy_olej',
              'Rajčatová_pasta', 'Droždí', 'Mozzarela',),  # H-Objekty v batohu
             ),
    ScenarioStep(tsTAKE, 'Vezmi Voda',  # Zadaný příkaz
             'Dal sis do batohu voda',
             'Byt',  # Aktuální prostor
             ('Ulice',),  # Aktuální sousedé
             ('Sůl', 'Klíče',),  # H-objekty v prostoru
             ('Peněženka', 'Mouka', 'Olivovy_olej',
              'Rajčatová_pasta', 'Droždí', 'Mozzarela',
              'Voda',),  # H-Objekty v batohu
             ),
    ScenarioStep(tsTAKE, 'Vezmi Sůl',  # Zadaný příkaz
             'Dal sis do batohu Sůl',
             'Byt',  # Aktuální prostor
             ('Ulice',),  # Aktuální sousedé
             ('Klíče',),  # H-objekty v prostoru
             ('Peněženka', 'Mouka', 'Olivovy_olej',
              'Rajčatová_pasta', 'Droždí', 'Mozzarela',
              'Voda', 'Sůl',),  # H-Objekty v batohu
             ),
    ScenarioStep(tsNS_0, 'Uhneť',  # Zadaný příkaz
             'Použil jsi vodu, sůl, mouku, droždí '
             'a olivový olej na unětění těsto',
             'Byt',  # Aktuální prostor
             ('Ulice',),  # Aktuální sousedé
             ('Klíče',),  # H-objekty v prostoru
             ('Peněženka', 'Rajčatová_pasta',
              'Mozzarela', 'Těsto'),  # H-Objekty v batohu
                 needs={'uhneteno' : False,},
                 tests=[ 'ingredients_present', ],
                 sets={'uhneteno' : True,},
             ),
    ScenarioStep(tsNS_1, 'Přidej Rajčatová_pasta',  # Zadaný příkaz
             'Na těsto bylo přidáno: Rajčatová_pasta',
             'Byt',  # Aktuální prostor
             ('Ulice',),  # Aktuální sousedé
             ('Klíče',),  # H-objekty v prostoru
             ('Peněženka', 'Mozzarela',
              'Těsto'),  # H-Objekty v batohu
                 needs={'uhneteno': True,
                        },
                tests=['dough_present', ],
                 sets={'Těsto.toppingcount' : 1,
                       },
             ),
    ScenarioStep(tsNS_1, 'Přidej Mozzarela',  # Zadaný příkaz
             'Na těsto bylo přidáno: mozzarela',
             'Byt',  # Aktuální prostor
             ('Ulice',),  # Aktuální sousedé
             ('Klíče',),  # H-objekty v prostoru
             ('Peněženka',
              'Těsto'),  # H-Objekty v batohu
                 needs={'uhneteno': True,},
                tests=['dough_present', ],
                 sets={'Těsto.toppingcount' : 2,},
             ),
    ScenarioStep(tsSUCCESS, 'Upeč',  # Zadaný příkaz
             'Vložil jsi použitelnou verzi pizzy do trouby\n'
             'Úspěšně jste ukončili hru.\n'
             'Děkujeme, že jste si zahráli.',
             'Byt',  # Aktuální prostor
             ('Ulice',),  # Aktuální sousedé
             ('Klíče',),  # H-objekty v prostoru
             ('Peněženka', 'Pizza'),  # H-Objekty v batohu
                 needs={
                        'Těsto.toppingcount' : 2,
                        },
                 tests=['dough_present', ],
                 sets={},
             ),

    )   # N-tice
)   # Konstruktor



############################################################################

ScenarioStep.next_index = +1  # Index prvního kroku za startem

BASIC = Scenario(stBASIC, (
    START_STEP,
    ScenarioStep(tsTAKE, 'Vezmi Klíče',  # Zadaný příkaz
         'Dal sis do batohu klíče',
         'Byt',  # Aktuální prostor
         ('Ulice',),  # Aktuální sousedé
         ('Peněženka', 'Sůl', 'Voda',),  # H-objekty v prostoru
         ('Klíče',),  # H-Objekty v batohu
         ),
    ScenarioStep(tsTAKE, 'Vezmi Peněženka',  # Zadaný příkaz
         'Dal sis do batohu Peněženka',
         'Byt',  # Aktuální prostor
         ('Ulice',),  # Aktuální sousedé
         ('Sůl', 'Voda',),  # H-objekty v prostoru
         ('Klíče', 'Peněženka',),  # H-Objekty v batohu
         ),
    ScenarioStep(tsGOTO, 'Jdi Ulice',  # Zadaný příkaz
         'Přesunul ses do prostoru:\n'
         'Ulice s lidmy, obchody a domy',
         'Ulice',  # Aktuální prostor
         ('Byt', 'Obchod_s_potravinami',),  # Aktuální sousedé
         (),  # H-objekty v prostoru
         ('Klíče', 'Peněženka',),  # H-Objekty v batohu
         ),
    ScenarioStep(tsGOTO, 'Jdi Obchod_s_potravinami',  # Zadaný příkaz
         'Přesunul ses do prostoru:\n'
         'Obchod se spoustou potravin',
         'Obchod_s_potravinami',  # Aktuální prostor
         ('Ulice', 'Oddělení_chlazenych', 'Regaly'),# Aktuální sousedé
         (),  # H-objekty v prostoru
         ('Klíče', 'Peněženka',),  # H-Objekty v batohu
         ),

    ScenarioStep(tsPUT_DOWN, 'Polož Klíče',        # Zadaný příkaz
        'Položil jsi předmět: klíče',
        'Obchod_s_potravinami',                   # Aktuální prostor
        ('Ulice', 'Oddělení_chlazenych', 'Regaly', ),  # Aktuální sousedé
        ('Klíče', ),         # H-objekty v prostoru
        ('Peněženka', ),                         # H-Objekty v batohu
        ),
    ScenarioStep(tsHELP, '?',                       # Zadaný příkaz
        SUBJECT,
        'Obchod_s_potravinami',                       # Aktuální prostor
        ('Ulice', 'Oddělení_chlazenych', 'Regaly',), # Aktuální sousedé
        ('Klíče',),         # H-objekty v prostoru
        ('Peněženka',),              # H-Objekty v batohu
        ),
    ScenarioStep(tsEND, 'KONEC',                    # Zadaný příkaz
        'Ukončili jste hru.\nDěkujeme, že jste si zahráli.',
        'Obchod_s_potravinami',                    # Aktuální prostor
        ('Ulice', 'Oddělení_chlazenych', 'Regaly', ), # Aktuální sousedé
        ('Klíče',),         # H-objekty v prostoru
        ('Peněženka', ),             # H-Objekty v batohu
        ),
    )   # N-tice
)   # Konstruktor



############################################################################
# Základní chybový scénář demonstrující průběh hry, při němž hráč
# zadává chybně příkazy k provedení základních akcí
# a současně vyzkouší vyvolání nápovědy a nestandardní ukončení.

ScenarioStep.next_index = -1  # Index kroku před korektním startem

WRONG_START = ScenarioStep(tsNOT_START, 'start', # Zadaný příkaz
        'Prvním příkazem není startovací příkaz.\n' 
        'Hru, která neběží, lze spustit pouze startovacím příkazem.\n',
        '',                                         # Aktuální prostor
        (),                                         # Aktuální sousedé
        (),                                         # H-objekty v prostoru
        (),                                         # H-Objekty v batohu
        )

ScenarioStep.next_index = +1  # Index prvního kroku za startem

MISTAKE = Scenario(stMISTAKES, (
    WRONG_START,
    START_STEP,
    ScenarioStep(tsEMPTY, '',                       # Zadaný příkaz
         ( erEMPTY := 'Prázdný příkaz lze použít pouze pro start hry'),
        'Byt',                                  # Aktuální prostor
        ('Ulice', ),                                  # Aktuální sousedé
        ('Sůl', 'Voda','Klíče','Peněženka',),   # H-objekty v prostoru
        (),                                         # H-Objekty v batohu
        ),
    ScenarioStep(tsUNKNOWN, 'maso',                 # Zadaný příkaz
        'Tento příkaz neznám: maso',
        'Byt',                                     # Aktuální prostor
        ('Ulice', ),                                  # Aktuální sousedé
        ('Sůl', 'Voda','Klíče','Peněženka', ),   # H-objekty v prostoru
        (),                                         # H-Objekty v batohu
        ),
    ScenarioStep(tsMOVE_WA, "jdi",                  # Zadaný příkaz
        'Nevím, kam mám jít.\n'
        'Je třeba zadat název cílového prostoru.',
        'Byt',                                   # Aktuální prostor
        ('Ulice', ),                                  # Aktuální sousedé
        ('Sůl', 'Voda','Klíče','Peněženka',  ),   # H-objekty v prostoru
        (),                                         # H-Objekty v batohu
        ),
    ScenarioStep(tsTAKE_WA, "vezmi",                # Zadaný příkaz
        'Nevím, co mám zvednout.\n'
        'Je třeba zadat název zvedaného objektu.',
        'Byt',                                 # Aktuální prostor
        ('Ulice',  ),                                  # Aktuální sousedé
        ('Sůl', 'Voda','Klíče','Peněženka',  ),   # H-objekty v prostoru
        (),                                         # H-Objekty v batohu
        ),
    ScenarioStep(tsPUT_DOWN_WA, "polož",            # Zadaný příkaz
        'Nevím, co mám položit.\n'
        'Je třeba zadat název pokládaného objektu.',
        'Byt',                                   # Aktuální prostor
        ('Ulice',),                                  # Aktuální sousedé
        ('Sůl', 'Voda','Klíče','Peněženka', ),   # H-objekty v prostoru
        (),                                         # H-Objekty v batohu
        ),
    ScenarioStep(tsBAD_NEIGHBOR, "jdi do_háje", # Zadaný příkaz
        'Do zadaného prostoru se odsud jít nedá: do_háje',
        'Byt',                                  # Aktuální prostor
        ('Ulice',),                                  # Aktuální sousedé
        ('Sůl', 'Voda','Klíče','Peněženka', ),   # H-objekty v prostoru
        (),                                         # H-Objekty v batohu
        ),
    ScenarioStep(tsBAD_ITEM, "vezmi whisky",        # Zadaný příkaz
        'Zadaný objekt v prostoru není: whisky',
        'Byt',                                 # Aktuální prostor
        ('Ulice', ),                                  # Aktuální sousedé
        ('Sůl', 'Voda','Klíče','Peněženka', ),   # H-objekty v prostoru
        (),                                         # H-Objekty v batohu
        ),


    ScenarioStep(tsTAKE, 'Vezmi Klíče',  # Zadaný příkaz
         'Dal sis do batohu klíče',
         'Byt',  # Aktuální prostor
         ('Ulice',),  # Aktuální sousedé
         ('Peněženka', 'Sůl', 'Voda',),  # H-objekty v prostoru
         ('Klíče',),  # H-Objekty v batohu
         ),
    ScenarioStep(tsTAKE, 'Vezmi Peněženka',  # Zadaný příkaz
         'Dal sis do batohu Peněženka',
         'Byt',  # Aktuální prostor
         ('Ulice',),  # Aktuální sousedé
         ('Sůl', 'Voda',),  # H-objekty v prostoru
         ('Klíče', 'Peněženka',),  # H-Objekty v batohu
         ),
    ScenarioStep(tsNOT_IN_BAG, 'polož panenka',     # Zadaný příkaz
        'Zadaný objekt v BAG není: panenka',
         'Byt',                                 # Aktuální prostor
        ('Ulice', ),                                  # Aktuální sousedé
        ('Sůl', 'Voda', ),                      # H-objekty v prostoru
        ('Klíče', 'Peněženka',),                      # H-Objekty v batohu
        ),
    ScenarioStep(tsGOTO, 'Jdi Ulice',  # Zadaný příkaz
         'Přesunul ses do prostoru:\n'
         'Ulice s lidmy, obchody a domy',
         'Ulice',  # Aktuální prostor
         ('Byt', 'Obchod_s_potravinami',),  # Aktuální sousedé
         (),  # H-objekty v prostoru
         ('Klíče', 'Peněženka',),  # H-Objekty v batohu
         ),
    ScenarioStep(tsGOTO, 'Jdi Obchod_s_potravinami',  # Zadaný příkaz
         'Přesunul ses do prostoru:\n'
         + (dOBCHOD := 'Obchod se spoustou potravin'),
         'Obchod_s_potravinami',  # Aktuální prostor
         ('Ulice', 'Oddělení_chlazenych', 'Regaly'),  # Aktuální sousedé
         (),  # H-objekty v prostoru
         ('Klíče', 'Peněženka',),  # H-Objekty v batohu
         ),
    ScenarioStep(tsGOTO, 'Jdi Regaly',  # Zadaný příkaz
         'Přesunul ses do prostoru:\n'
         + (dREGALY := 'Regaly s jidlem ktere nepotrebuje chladit'),
         'Regaly',  # Aktuální prostor
         ('Oddělení_chlazenych', 'Obchod_s_potravinami',),
         # Aktuální sousedé
         ('Mouka', 'Cukr', 'Droždí', 'Olivovy_olej',
          'Rajčatová_pasta', 'Česknek', 'Olivy',
          'Cibule', 'Kukuřice', 'Bazalka', 'Ananas',),
         # H-objekty v prostoru
         ('Klíče', 'Peněženka',),  # H-Objekty v batohu
         ),

        ScenarioStep(tsUNMOVABLE, "vezmi Mouka", # Zadaný příkaz
         'Zadaný objekt není možno zvednout: Mouka',
         'Regaly',  # Aktuální prostor
         ('Oddělení_chlazenych', 'Obchod_s_potravinami',),
         # Aktuální sousedé
         ('Mouka', 'Cukr', 'Droždí', 'Olivovy_olej',
          'Rajčatová_pasta', 'Česknek', 'Olivy',
          'Cibule', 'Kukuřice', 'Bazalka', 'Ananas',),
         # H-objekty v prostoru
         ('Klíče', 'Peněženka',),  # H-Objekty v batohu
         ),
        #Musel jsem dat do MISTAKE scenare custom prikaz, protoze jen ten
        # operuje s mym ekvivalentem kapacity batohu - penezy na nakup

        ScenarioStep(tsBAG_FULL, 'Kup Cibule',  # Zadaný příkaz
         'Nelze koupit předmět, na který nemáš: Cibule',
         'Regaly',  # Aktuální prostor
         ('Oddělení_chlazenych', 'Obchod_s_potravinami',),
         # Aktuální sousedé
         ('Mouka', 'Cukr', 'Droždí', 'Olivovy_olej',
          'Rajčatová_pasta', 'Česknek', 'Olivy',
          'Cibule', 'Kukuřice', 'Bazalka', 'Ananas',),
         # H-objekty v prostoru
         ('Klíče', 'Peněženka',),  # H-Objekty v batohu
         ),
    ScenarioStep(tsHELP, '?',                       # Zadaný příkaz
        SUBJECT,
         'Regaly',  # Aktuální prostor
         ('Oddělení_chlazenych', 'Obchod_s_potravinami',),
         # Aktuální sousedé
         ('Mouka', 'Cukr', 'Droždí', 'Olivovy_olej',
          'Rajčatová_pasta', 'Česknek', 'Olivy',
          'Cibule', 'Kukuřice', 'Bazalka', 'Ananas',),
         # H-objekty v prostoru
         ('Klíče', 'Peněženka',),  # H-Objekty v batohu
         ),
    ScenarioStep(tsEND, 'KONEC',                    # Zadaný příkaz
        'Ukončili jste hru.\n'
        'Děkujeme, že jste si zahráli.',
         'Regaly',  # Aktuální prostor
         ('Oddělení_chlazenych', 'Obchod_s_potravinami',),
         # Aktuální sousedé
         ('Mouka', 'Cukr', 'Droždí', 'Olivovy_olej',
          'Rajčatová_pasta', 'Česknek', 'Olivy',
          'Cibule', 'Kukuřice', 'Bazalka', 'Ananas',),
         # H-objekty v prostoru
         ('Klíče', 'Peněženka',),  # H-Objekty v batohu
         ),
    )   # N-tice
)   # Konstruktor



############################################################################
# Základní chybový scénář demonstrující průběh hry, při němž hráč
# zadává chybně příkazy k provedení povinně definovaných akcí.
ScenarioStep.next_index = 5    # Index prvního nestandardního kroku
MISTAKE_NS = Scenario(stMISTAKES_NS, (
    HAPPY.steps[0],
    ScenarioStep(tsNS0_WrongCond, 'Uhneť',  # Zadaný příkaz
         'Nekoupil jsi mouku, olej nebo drozdi, nemuzes uhneť',
         'Byt',  # Aktuální prostor
         ('Ulice',),  # Aktuální sousedé
         ('Sůl', 'Voda', 'Klíče', 'Peněženka',),  # H-objekty v prostoru
         (),  # H-Objekty v batohu
         # H-Objekty v batohu
         tests=['ingredients_present', ],
         ),
    ScenarioStep(tsNOT_SUCCESS, 'Upeč',        # Zadaný příkaz
        'Nemáš připravenou pizzu k Upeč',
         'Byt',  # Aktuální prostor
         ('Ulice',),  # Aktuální sousedé
         ('Sůl', 'Voda', 'Klíče', 'Peněženka',),  # H-objekty v prostoru
         (),  # H-Objekty v batohu

        tests = ['dough_present', ],
        ),
    ScenarioStep(tsNS0_WrongCond, 'Uhneť',  # Zadaný příkaz
         'Nekoupil jsi mouku, olej nebo drozdi, nemuzes uhneť',
         'Byt',  # Aktuální prostor
         ('Ulice',),  # Aktuální sousedé
         ('Sůl', 'Voda', 'Klíče', 'Peněženka',),  # H-objekty v prostoru
         (),  # H-Objekty v batohu
         # H-Objekty v batohu
         tests=['ingredients_present', ],
         ),
    ScenarioStep(tsNS1_WrongCond, 'Kup Sůl',  # Zadaný příkaz
     (NS1_WRONG_ARGb := 'Nelze koupit objekt ') + 'Sůl',
     'Byt',  # Aktuální prostor
     ('Ulice',),  # Aktuální sousedé
     ('Sůl', 'Voda', 'Klíče', 'Peněženka',),
     (),  # H-Objekty v batohu
     tests=['argument_buyable'],
     ),
    HAPPY.steps[1],   # Vezmi Klíče
    HAPPY.steps[2],   # Vezmi Peněženka
    HAPPY.steps[3],   # Jdi Ulice
    HAPPY.steps[4],   # Jdi Obchod_s_potravinami
    HAPPY.steps[5],   # Jdi Regaly

    ScenarioStep(tsNS1_0Args, 'Kup',  # Zadaný příkaz
     'Nevím, co mám koupit',
     'Regaly',  # Aktuální prostor
     ('Oddělení_chlazenych', 'Obchod_s_potravinami',), # Aktuální sousedé
     ('Mouka', 'Cukr', 'Droždí', 'Olivovy_olej',
      'Rajčatová_pasta', 'Česknek', 'Olivy',
      'Cibule', 'Kukuřice', 'Bazalka', 'Ananas',),
     ('Klíče','Peněženka',),  # H-Objekty v batohu
     ),
    ScenarioStep(tsNS1_WrongCond, 'Kup Voda',  # Zadaný příkaz
     'Zadaný objekt v prostoru není: voda',
     'Regaly',  # Aktuální prostor
     ('Oddělení_chlazenych', 'Obchod_s_potravinami',),  # Aktuální sousedé
     ('Mouka', 'Cukr', 'Droždí', 'Olivovy_olej',
      'Rajčatová_pasta', 'Česknek', 'Olivy',
      'Cibule', 'Kukuřice', 'Bazalka', 'Ananas',),
     ('Klíče','Peněženka',),  # H-Objekty v batohu
     tests=['argument_present', ],
     ),

    ScenarioStep(tsNS1_WrongCond, 'Kup Mozzarela',  # Zadaný příkaz
     'Zadaný objekt v prostoru není: Mozzarela',
     'Regaly',  # Aktuální prostor
     ('Oddělení_chlazenych', 'Obchod_s_potravinami',),  # Aktuální sousedé
     ('Mouka', 'Cukr', 'Droždí', 'Olivovy_olej',
      'Rajčatová_pasta', 'Česknek', 'Olivy',
      'Cibule', 'Kukuřice', 'Bazalka', 'Ananas',),  # H-objekty v prostoru
     ('Klíče','Peněženka',),
     # H-Objekty v batohu

     tests=['argument_present', ],

     ),
    HAPPY.steps[6],  # Kup mouka
    HAPPY.steps[7],  # Kup Olivovy_olej
    HAPPY.steps[8],  # Kup Rajčatová_pasta
    HAPPY.steps[9],  # Kup Droždí
    HAPPY.steps[10],  # Jdi Oddělení_chlazenych
    HAPPY.steps[11],  # Kup Mozzarela

    ScenarioStep(tsNS1_WrongCond, 'Kup Kukuřice', # Zadaný příkaz
        'Zadaný objekt v prostoru není: kukuřice',
         'Oddělení_chlazenych',  # Aktuální prostor
         ('Regaly', 'Obchod_s_potravinami'),  # Aktuální sousedé
         ('Šunka', 'Salám', 'Mozzarela',),  # H-objekty v prostoru
         ('Klíče', 'Peněženka', 'Mouka', 'Olivovy_olej',
          'Rajčatová_pasta', 'Droždí', 'Mozzarela',),
         # H-Objekty v batohu
        tests=['argument_present', ],
        ),
    ScenarioStep(tsNS1_WrongCond, 'Kup Salám',  # Zadaný příkaz
         'Nelze koupit předmět, na který nemáš: Salám',
         'Oddělení_chlazenych',  # Aktuální prostor
         ('Regaly', 'Obchod_s_potravinami'),  # Aktuální sousedé
         ('Šunka', 'Salám', 'Mozzarela',),  # H-objekty v prostoru
         ('Klíče', 'Peněženka', 'Mouka', 'Olivovy_olej',
          'Rajčatová_pasta', 'Droždí', 'Mozzarela',),
         # H-Objekty v batohu
         needs={'Peněženka.balance': 150, }
         ),
    HAPPY.steps[12],  # Jdi Obchod_s_potravinami
    HAPPY.steps[13],  # Jdi Ulice
    HAPPY.steps[14],  # Jdi Byt
    HAPPY.steps[15],  # Poloz klice
    HAPPY.steps[16],  # Vezmi Sul
    HAPPY.steps[17],  # Vezmi Voda
    ScenarioStep(tsNS1_WrongCond, 'Přidej Salám',  # Zadaný příkaz
         'Neni uhnetene testo, nelze Přidej',
         'Byt',  # Aktuální prostor
         ('Ulice',),  # Aktuální sousedé
         ('Klíče',),  # H-objekty v prostoru
         ('Peněženka', 'Mouka', 'Olivovy_olej',
          'Rajčatová_pasta', 'Droždí', 'Mozzarela',
          'Voda', 'Sůl',),  # H-Objekty v batohu
         # H-Objekty v batohu
         needs={'uhneteno': True, }
         ),
    HAPPY.steps[18],  # Uhnet

    ScenarioStep(tsNS0_WrongCond, 'Uhneť',  # Zadaný příkaz
     'Uz mas hotove testo, nepotrebujes znovu Uhněť',
     'Byt',  # Aktuální prostor
     ('Ulice',),  # Aktuální sousedé
     ('Klíče',),  # H-objekty v prostoru
     ('Peněženka', 'Rajčatová_pasta',
      'Mozzarela', 'Těsto'),  # H-Objekty v batohu
     needs={'uhneteno': False, },

     ),
    ScenarioStep(tsNOT_SUCCESS, 'Upeč',  # Zadaný příkaz
     'Nemáš připravenou pizzu k Upeč',
     'Byt',  # Aktuální prostor
     ('Ulice',),  # Aktuální sousedé
     ( 'Klíče', ),  # H-objekty v prostoru
     ('Peněženka', 'Rajčatová_pasta',
              'Mozzarela', 'Těsto'),  # H-Objekty v batohu
        needs={'Těsto.toppingcount' : 2,},

     ),
    HAPPY.steps[19],  # Přidej rajčatova pasta
    HAPPY.steps[20],  # Přijdej mozzarela

    ScenarioStep(tsNS1_WrongCond, 'Přidej Salám',  # Zadaný příkaz
     'Nelze přidat nepřítomný objekt: Salám',
     'Byt',  # Aktuální prostor
     ('Ulice',),  # Aktuální sousedé
     ('Klíče',),  # H-objekty v prostoru
     ('Peněženka',
     'Těsto'),  # H-Objekty v batohu
     tests=['argument_present', ],
     ),

    ScenarioStep(tsNS1_WrongCond, 'Přidej Mozzarela',  # Zadaný příkaz
    'Nelze přidat nepřítomný objekt: Mozzarela',
     'Byt',  # Aktuální prostor
     ('Ulice',),  # Aktuální sousedé
     ('Klíče',),  # H-objekty v prostoru
     ('Peněženka',
      'Těsto'),  # H-Objekty v batohu
    tests=['argument_present', ],
    ),

    ScenarioStep(tsNS1_WrongCond, 'Přidej Rajčatová_pasta',  # Zadaný příkaz
     'Nelze přidat nepřítomný objekt: Rajčatová_pasta',
     'Byt',  # Aktuální prostor
     ('Ulice',),  # Aktuální sousedé
     ('Klíče',),  # H-objekty v prostoru
     ('Peněženka',
      'Těsto'),  # H-Objekty v batohu
        tests=['argument_present', ],

     ),

    ScenarioStep(tsNS1_0Args, 'Přidej',  # Zadaný příkaz
         'Nevím co mám Přidej',
         'Byt',  # Aktuální prostor
         ('Ulice',),  # Aktuální sousedé
         ('Klíče',),  # H-objekty v prostoru
         ('Peněženka',
          'Těsto'),  # H-Objekty v batohu
         ),

    ScenarioStep(tsEND, 'konec',                    # Zadaný příkaz
        'Ukončili jste hru.\n'
        'Děkujeme, že jste si zahráli.',
        'Byt',                       # Aktuální prostor
        ('Ulice',),  # Aktuální sousedé
        ('Klíče', ),
        ('Peněženka',
              'Těsto'),  # H-Objekty v batohu
        ),
    )   # N-tice
)   # Konstruktor



###########################################################################q

# Slovník převádějící názvy scénářů na scénáře
NAME_2_SCENARIO = {
    HAPPY       .name: HAPPY,     # Základní úspěšný (= šťastný) scénář
    BASIC       .name: BASIC,     # Scénář obsahující jen povinné akce
    MISTAKE     .name: MISTAKE,   # Scénář chybně zadaných povinných akcí
    MISTAKE_NS  .name: MISTAKE_NS,# Scénář chybně zadaných dodatečných akcí
}



###########################################################################q
dbg.stop_mod(1, __name__)
