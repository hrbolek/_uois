from doctest import master
from functools import cache
from gql_personalities.DBDefinitions import BaseModel, UserModel, Personalities_RankHistory, Personalities_Study, Personalities_Certificate, Personalities_Medal, Personalities_WorkHistory, Personalities_RelatedDoc
from gql_personalities.DBDefinitions import Personalities_CertificateType, Personalities_MedalType
from gql_personalities.DBDefinitions import Personalities_MedalTypeGroup

import random
import itertools
from functools import cache


from sqlalchemy.future import select

def singleCall(asyncFunc):
    """Dekorator, ktery dovoli, aby dekorovana funkce byla volana (vycislena) jen jednou. Navratova hodnota je zapamatovana a pri dalsich volanich vracena.
       Dekorovana funkce je asynchronni.
    """
    resultCache = {}
    async def result():
        if resultCache.get('result', None) is None:
            resultCache['result'] = await asyncFunc()
        return resultCache['result']
    return result

###########################################################################################################################
#
# zde definujte sve funkce, ktere naplni random data do vasich tabulek
#
###########################################################################################################################
@cache
def determineCertificateTypes():
    certificateTypes = [
        {'name': 'jazykové', 'en_name': 'language', 'id': 'db9ba8c3-3d6e-4190-bfe7-d401586dd282'},
        {'name': 'vědecké', 'en_name': 'science', 'id': 'bc988cb6-38a7-45a1-97ec-d1e220621355'},
        {'name': 'sportovní', 'en_name': 'sport', 'id': '3f1351ca-0624-43bb-9c93-23e6478fb1c1'},
        {'name': 'pracovní', 'en_name': 'work', 'id': 'e4713dd6-69e6-4d35-964b-1bca141899eb'}
    ]
    return certificateTypes

@cache
def determineMedalTypes():
    medalTypes = [
        #Řády a vyznamenání České republiky
        {'name': 'Řád Bílého lva', 'id': 'cf4c274c-6cf1-11ed-a1eb-0242ac120002' },
        {'name': 'Řád Tomáše Garrigua Masaryka', 'id': 'cf4c2ef4-6cf1-11ed-a1eb-0242ac120002'},
        {'name': 'Medaile za hrdinství', 'id': 'cf4c3052-6cf1-11ed-a1eb-0242ac120002'},
        {'name': 'Medaile za zásluhy', 'id': 'cf4c3188-6cf1-11ed-a1eb-0242ac120002'},

        #Vojenské resortní vyznamenání
        {'name': 'Záslužný kříž', 'id': '1ebfcc2a-6cf2-11ed-a1eb-0242ac120002' },
        {'name': 'Medaile za zranění', 'id': '1ebfcf2c-6cf2-11ed-a1eb-0242ac120002'},
        {'name': 'Medaile ministra obrany za službu v zahraničí', 'id': '1ebfd076-6cf2-11ed-a1eb-0242ac120002'},
        {'name': 'Medaile Armády České republiky', 'id': '1ebfd198-6cf2-11ed-a1eb-0242ac120002'},

        #Čestné odznaky
        {'name': 'Čestný pamětní odznak za službu míru', 'id': '97edb3fc-a4d2-4295-a8ca-e7e97fba87e1' },
        {'name': 'Čestný pamětní odznak za službu v misi IFOR', 'id': '159c84ce-3a57-423a-8e1b-c49ce19cd02a' },
        {'name': 'Čestný pamětní odznak 50 let NATO', 'id': 'e8b157e2-30bf-4100-8449-60c9eea26018' },
        {'name': 'Čestný pamětní odznak 10 let školícího a vzdělávacího střediska Ministerstva obrany Komorní Hrádek', 'id': '62993164-aa76-4fcd-ab77-960f3b433e49' },
        {'name': 'Pamětní odznak Summit NATO Praha 2002', 'id': '9638bdbd-3fa4-4a5e-9295-e15fd57765c6' },
        {'name': 'Pamětní odznak NATO 1999-2004', 'id': 'bc24e3df-5b18-4b19-933a-915b462f7d71' },
        {'name': 'Pamětní medaile k 60. ukončení 2. světové války', 'id': '6b3ea765-11e4-4ca0-9bbf-698c9d6d44d2' },
        {'name': 'Pamětní odznak Vojenské akademie v Brně 1951-2004', 'id': '11a8b0fd-f739-4293-9d8e-3f526aee2fc3' },
        {'name': 'Čestný odznak Přemysla Otakara II., krále železného a zlatého', 'id': 'e1bbcb9b-91d3-498c-83ad-82dc168475d2' },
        {'name': 'Pamětní odznak štábního kapitána Václava Morávka', 'id': 'dfa459de-63c4-4654-9eba-2c90bf1124c7' },
        {'name': 'Pamětní odznak 4. brigády rychlého nasazení "Obrany národa"', 'id': '33fb8070-b5da-45f9-93a4-abceb1a54fd3' },
        {'name': 'Čestný pamětní odznak k 50. výročí vzniku čs. výsadkového vojska', 'id': 'aa5f8d02-333b-45ee-9fc1-854fa3103b62' },
        {'name': 'Čestný pamětní odznak za službu v misi SFOR', 'id': '5e8ca930-4876-4360-ba3d-52ba1bb0b62e' },
        {'name': 'Čestný pamětní odznak za službu v mírové misi na Balkáně', 'id': 'df5cfa34-66d6-47db-8714-24c7478490a8' },
        {'name': 'Čestný pamětní odznak k 10. výročí války v Perském zálivu', 'id': 'd05662aa-3593-4ffc-bf7b-2d54b7ca336f' },
        {'name': 'Pamětní odznak vojenské logistiky', 'id': 'a7dde577-8b5a-485d-8eea-f0f57512e49b' },
        {'name': 'Pamětní odznak 4. průzkumného praporu Bechyně', 'id': '6afa9a62-822f-4c89-91d7-573dbf089606' },
        {'name': 'Čestný odznak generála JUDr. Viktora Spěváčka', 'id': '32526f1a-8d94-4f62-b2d0-5564c9ff79b0' },
        {'name': 'Pamětní odznak velitelství vzdušných sil', 'id': '7d94ba3e-569d-461d-9a74-f969f259b35d' },
        {'name': 'Pamětní odznak metrologie a technického dozoru', 'id': 'b532f548-2151-405c-83b1-04eb10678ced' },
        {'name': 'Pamětní odznak Ústřední opravárenské základny automibilní techniky', 'id': '3d6c001f-701e-4d7b-8a3d-86558b26b7b7' },
        {'name': 'Pamětní odznak Ústřední opravárenské základny prostředků velení', 'id': '2f90938f-9347-4e51-a3d6-8c8bb3b64501' },
        {'name': 'Pamětní odznak Automobilního skladu Nový Jičín', 'id': 'c684f1d4-96df-49a3-bb96-a8220f5560ac' },
        {'name': 'Pamětní odznak Vojenské akademie Vyškov', 'id': '9f7c68ab-63e1-47a9-889e-6ef3ab13399b' },
        {'name': 'Pamětní odznak Ústřední základny zbraní a zbraňových systémů', 'id': '6ea03605-375f-48c1-a3b3-6430edda5f58' },
        {'name': 'Pamětní odznak Ústřední opravárenské základny zbraní a zbraňových systémů', 'id': '233e68ab-8f56-4b93-8b63-52b42da0c5d7' },
        {'name': 'Pamětní odznak 7. polní nemocnice', 'id': 'd61eef29-8b1b-45b5-8ddc-1843cdcbaebd' },
        {'name': 'Pamětní odznak Výcvikové základny mírových sil Český Krumlov', 'id': 'b682aa69-e877-4822-a473-b8e15f881f32' },
        {'name': 'Pamětní odznak střediska Centre of Excellence', 'id': 'aa96f62f-2836-449d-a48a-a873425ba80f' },
        {'name': 'Pamětní odznak Vojenské policie - Irák', 'id': '05d7c18f-649e-483b-9e26-0c055528aca5' },
        {'name': 'Pamětní odznak Střední technické školy', 'id': '972b27d9-1e11-424e-bdd3-4f08f48c555c' },
        {'name': 'Pamětní odznak 5. dopravní základny logistické a zdravotnické podpory', 'id': '1dbaddb5-07f6-4bc4-922e-2d444e945ee9' },
        {'name': 'Pamětní odznak Výzkumného střediska Doksy', 'id': 'a482970b-f29d-4de7-a71a-abdcd403c87e' },
        {'name': 'Pamětní odznak Speciálních sil mise Enduring Freedom z Afghánistánu', 'id': '2301eb86-2d8d-4da1-9ad3-78d9b5b5871b' },
        {'name': 'Pamětní odznak Vojenské lékařské akademie J. E. Purkyně', 'id': '96ddedbb-d4e8-411b-8773-8f1adda1782b' },
        {'name': 'Pamětní odznak Ústřední základny materiálu všeobecného použití', 'id': 'fa838268-8a26-46fc-b36d-a8032ac4e682' },
        {'name': 'Pamětní odznak 2. mechnizované brigády Písek', 'id': 'c5c2d05b-1977-4ff2-b027-218a703c57d9' },
        {'name': 'Pamětní odznak Letecké opravárenské základny Brno', 'id': '7b751e5f-bc44-4a04-847b-3b776dd2d298' },
        {'name': 'Pamětní odznak 601. skupiny speciálních sil', 'id': '93b8b1af-d91f-4676-ac75-d374c8dc78a1' },
        {'name': 'Pamětní odznak Ústřední opravárenské základny materiálu osobního použití Chrudim', 'id': 'bbbef578-0a80-4c81-a56b-a7b7ec6576f2' },
        {'name': 'Pamětní odznak KFOR', 'id': 'efb084a0-7a87-464e-8ecd-7596fb9337c9' },
        {'name': 'Pamětní odznak veterinární základny Grabštejn', 'id': 'bf8af41c-ef71-43cb-9a69-fc7e01efccf7' },
        {'name': 'Pamětní odznak 51. NPP Pardubice', 'id': 'fa11b6df-8f45-4f00-80f5-22805108113b' },
        {'name': 'Pamětní odznak 7. mechanizované brigády „Dukelské“ Hranice', 'id': 'e0bbb6f3-341c-450c-ac33-f4662eac270c' },
        {'name': 'Pamětní odznak Hradní stráže', 'id': '752bb4ee-f9ac-446d-bbb8-2592ce3ade79' },
        {'name': 'Pamětní odznak Inspekce MO a bývalého ÚřK BVLSI', 'id': '0f682be0-bb44-40fd-85b6-8eed606ca329' },
        {'name': 'Pamětní odznak pro 312. prapor chemické ochrany NATO za službu v jednotkách NRF', 'id': 'fbc8a9e0-8695-4a06-93ad-915065b04d91' },
        {'name': 'Pamětní odznak Vojenské střední školy Vyškov', 'id': '36e1bc46-472c-4d43-b272-1fb994d581c6' }
       
    ]
    return medalTypes


@cache
def determineMedalTypeGroup():
    medalTypeGroup = [
        {'name': 'Řády a vyznamenání České republiky', 'id': '0747704c-d6f9-461c-9b2f-4b9681bd50ed' },
        {'name': 'Vojenské resortní vyznamenání', 'id': '2c34f055-d2fa-4eb1-a29a-ed28a2277e6c'},
        {'name': 'Čestné odznaky', 'id': '6299630e-4d27-44a9-a844-53831add33ca'}
    ]
    return medalTypeGroup

