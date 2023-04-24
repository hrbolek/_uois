from functools import cache
from gql_personalities.DBDefinitions import (
    
    RankModel,
    StudyModel,
    CertificateModel,
    MedalModel,
    WorkHistoryModel,
    RelatedDocModel,
    RankTypeModel, 
    CertificateTypeModel, 
    MedalTypeModel, 
    MedalTypeGroupModel,
    CertificateTypeGroupModel
)

from functools import cache


from sqlalchemy.future import select


def singleCall(asyncFunc):
    """Dekorator, ktery dovoli, aby dekorovana funkce byla volana (vycislena) jen jednou. Navratova hodnota je zapamatovana a pri dalsich volanich vracena.
    Dekorovana funkce je asynchronni.
    """
    resultCache = {}

    async def result():
        if resultCache.get("result", None) is None:
            resultCache["result"] = await asyncFunc()
        return resultCache["result"]

    return result


###########################################################################################################################
#
# zde definujte sve funkce, ktere naplni random data do vasich tabulek
#
###########################################################################################################################
def get_demodata(asyncSessionMaker):
    pass


@cache
def determineRankType():
    rankTypes = [
        # mužstvo
        {
            "name": "vojín (voj.)",
            "name_en": "Private (PVT)",
            "id": "de5e6ae8-902c-4b06-aa8e-8fbca99026f3",
        },
        {
            "name": "svobodník (svob.)",
            "name_en": "Private First Class (PFC)",
            "id": "f3038058-e1fa-4f7c-9e50-7b1d99998d37",
        },
        # poddůstojníci
        {
            "name": "desátník (des.)",
            "name_en": "Corporal (CPL)",
            "id": "a3cdae76-1c7d-409c-8bed-9e922c066bce",
        },
        {
            "name": "četař (čet.)",
            "name_en": "Sergeant (SGT)",
            "id": "a17e81a6-776b-4883-a04d-cbd4f07ad095",
        },
        {
            "name": "rotný (rtn.)",
            "name_en": "Staff Sergeant (SSG)",
            "id": "a9043224-9c3b-4562-a329-997fba9237d0",
        },
        # praporčíci
        {
            "name": "rotmistr (rtm.)",
            "name_en": "Sergeant First Class (SFC)",
            "id": "72294ac5-1823-4164-9805-60a0aaa39296",
        },
        {
            "name": "nadrotmistr (nrtm.)",
            "name_en": "Master Sergeant (MSG)",
            "id": "453dff9e-fab2-41d0-8bef-ca76c78e79c8",
        },
        {
            "name": "praporčík (prap.)",
            "name_en": "Chief Warrant Officer (CW2)",
            "id": "6a324f4a-2162-4fe7-a47c-8be1f3c9452b",
        },
        {
            "name": "nadpraporčík (nprap.)",
            "name_en": "Chief Warrant Officer (CW3)",
            "id": "34cfd57e-6a09-4423-8025-b44d6dbce774",
        },
        {
            "name": "štábní praporčík (št. prap.)",
            "name_en": "Master Warrant Officer (MW4)",
            "id": "841fa09f-625e-49b4-8872-05c43ce197cf",
        },
        # nižší důstojníci
        {
            "name": "poručík (por.)",
            "name_en": "Lieutenant (LT)",
            "id": "3914ab9f-78bc-45ac-bb2d-59ee921f3a19",
        },
        {
            "name": "nadporučík (npor.)",
            "name_en": "First Lieutenant (1LT)",
            "id": "437fa94e-8442-4667-af9a-8327afef9ffa",
        },
        {
            "name": "kapitán (ktp.)",
            "name_en": "Captain (CPT)",
            "id": "a8ce2853-26ec-4e10-8bbe-899cc296a35f",
        },
        # vyšší důstojníci
        {
            "name": "major (mjr.)",
            "name_en": "Major (MAJ)",
            "id": "587cd381-aeec-4367-91f3-8849f900848a",
        },
        {
            "name": "podplukovník (pplk.)",
            "name_en": "Lieutenant Colonel (LTC)",
            "id": "46a7325f-9b9e-4e80-9f17-670bd9151229",
        },
        {
            "name": "plukovník (plk.)",
            "name_en": "Colonel (COL)",
            "id": "824533e5-eba7-45f7-80f6-e2466529e73c",
        },
        # generálové
        {
            "name": "brigádní generál (brig.gen.)",
            "name_en": "Brigadier General (BG)",
            "id": "9eb8d8f4-a87c-447d-aaee-c0a15cd6fbce",
        },
        {
            "name": "generálmajor (genmjr.)",
            "name_en": "Major General (MG)",
            "id": "d65a0d25-dc39-46fa-a107-a684c9724c5e",
        },
        {
            "name": "generálporučík (genpor.)",
            "name_en": "Lieutenant General (LTG)",
            "id": "41f0772d-738a-492d-93c1-96c9cdb5d597",
        },
        {
            "name": "armádní generál (arm.gen.)",
            "name_en": "General of the Army (GA)",
            "id": "9234d06c-e811-4016-8ee5-f6975b4048a4",
        },
    ]
    return rankTypes


@cache
def determineStudyPlace():
    studyPlaces = [
        # veřejné VŠ
        {
            "name": "Akademie múzických umění v Praze (AMU)",
            "id": "88556487-cbf0-46ec-889a-71720b93ea37",
        },
        {
            "name": "Akademie výtvarných umění v Praze (AVU)",
            "id": "2b84e0ab-fe7b-4104-8601-4553caa0f83d",
        },
        {
            "name": "Česká zemědělská univerzita v Praze (ČZU)",
            "id": "db8a49b1-5c1d-4681-b964-8a32db02c0a0",
        },
        {
            "name": "České vysoké učení technické v Praze (ČVUT)",
            "id": "635135dc-f119-4a1c-88dd-f5fc8395f501",
        },
        {
            "name": "Janáčkova akademie múzických umění (JAMU)",
            "id": "10f191ae-284f-44ed-90ce-29b3cdadc070",
        },
        {
            "name": "Jihočeská univerzita v Českých Budějovicích (JU)",
            "id": "4bdb5ce2-ad70-4c2b-9ba5-516d3df3fb3b",
        },
        {
            "name": "Masarykova univerzita (MU)",
            "id": "782e1ee1-9f15-46bd-8e74-3e546c9afd37",
        },
        {
            "name": "Mendelova univerzita v Brně (MENDELU)",
            "id": "258f8f4e-a7f2-418f-bdd9-cfbbf8f38099",
        },
        {
            "name": "Ostravská univerzita (OU)",
            "id": "0a9d1130-5bc2-4de2-92a1-8c1be055e707",
        },
        {
            "name": "Slezská univerzita v Opavě (SU)",
            "id": "d51f4119-0918-4427-ad36-27818dc49bc3",
        },
        {
            "name": "Technická univerzita v Liberci (TUL)",
            "id": "6a059f6f-16d9-4cb8-94ac-084d6165a345",
        },
        {
            "name": "Univerzita Hradec Králové (UHK)",
            "id": "b8491178-53fd-4b6b-84cb-5cb8d859d489",
        },
        {
            "name": "Univerzita Jana Evangelisty Purkyně v Ústí nad Labem (UJEP)",
            "id": "236a2e9f-010c-443c-84e7-52973e8094fd",
        },
        {
            "name": "Univerzita Karlova (UK)",
            "id": "94115ab6-0443-473c-b66e-0c6d29572c89",
        },
        {
            "name": "Univerzita Palackého v Olomouci (UP)",
            "id": "e7e69091-982b-4f0c-80ad-a5bb074ef5bd",
        },
        {
            "name": "Univerzita Pardubice (UPCE)",
            "id": "c2886fd7-c3df-470a-9abc-25617e838453",
        },
        {
            "name": "Univerzita Tomáše Bati ve Zlíně (UTB, zkrácený název: UTB ve Zlíně)",
            "id": "533ed300-f78e-4f8e-abb1-7b039ff63438",
        },
        {
            "name": "Veterinární univerzita Brno (VETUNI)",
            "id": "a8f84591-d060-4763-8b95-890f5e9e9dc1",
        },
        {
            "name": "Vysoká škola báňská - Technická univerzita Ostrava (VŠB-TUO, zkrácený název: VŠB - Technická univerzita Ostrava)",
            "id": "c63b55eb-c6a0-4302-aa27-3ff8f082cc35",
        },
        {
            "name": "Vysoká škola ekonomická v Praze (VŠE)",
            "id": "b38fc480-98bd-4a9c-8b3f-58a0eff3506c",
        },
        {
            "name": "Vysoká škola chemicko-technologická v Praze (VŠCHT Praha)",
            "id": "cce2633e-a059-4b72-92d3-52652f6bc07c",
        },
        {
            "name": "Vysoká škola polytechnická Jihlava (VŠPJ či VŠP Jihlava)",
            "id": "9f128a38-6405-4435-a4f2-be7050755a2e",
        },
        {
            "name": "Vysoká škola technická a ekonomická v Českých Budějovicích (VŠTE)",
            "id": "8e1c2c35-50fd-40b6-9cd9-cad795f20dbf",
        },
        {
            "name": "Vysoká škola uměleckoprůmyslová v Praze (UMPRUM)",
            "id": "4c807453-dd9d-455f-a334-f4007f2bbefc",
        },
        {
            "name": "Vysoké učení technické v Brně (VUT)",
            "id": "4bb8f25a-79e5-493a-9b52-dbb2855537b8",
        },
        {
            "name": "Západočeská univerzita v Plzni (ZČU)",
            "id": "fbad1416-2f46-4671-927c-100be0914dcb",
        },
        # státní VŠ
        {
            "name": "Policejní akademie České republiky v Praze (POLAC)",
            "id": "31a7d00f-de73-4d70-9e02-a139d0a3096c",
        },
        {
            "name": "Univerzita obrany (UNOB)",
            "id": "3da845f7-a616-4ed9-98d8-329fac7fae81",
        },
    ]
    return studyPlaces


@cache
def determineStudyProgram():
    studyPrograms = [
        {
            "name": "bakalářský",
            "name_en": "bachelor",
            "id": "00602448-9d42-4af3-95fd-20fd6a551771",
        },
        {
            "name": "magisterský",
            "name_en": "master",
            "id": "f0e17944-e7d8-434a-9b36-b70cf6f0fac5",
        },
        {
            "name": "doktorský",
            "name_en": "doctoral",
            "id": "0ea55a54-1fa5-43ce-b2e6-67ebf57c9671",
        },
    ]
    return studyPrograms


@cache
def determineCertificateType():
    certificateTypes = [
        # jazykové
        {"name": "STANAG English", "id": "34a29ef9-b9a9-4d62-9270-e16504d47fa9"},
        {"name": "PET", "id": "8f212ce5-9dfb-4595-a3c0-8c819a6af424"},
        {"name": "CAE", "id": "9ab4186a-1a23-4632-8dc5-8b6c7012c024"},
        {"name": "FCE", "id": "228ad8c0-8ef9-48ec-9ad1-fa9e9c123d50"},
        {"name": "CPE", "id": "6bc6e441-511c-403b-a754-50b8ccd9bfc3"},
        {"name": "TOEFL", "id": "87408450-922a-4f2e-84c5-3fd25255d738"},
        {"name": "IELTS", "id": "6c2b6c8f-812f-4372-bd10-1a395c7faf4b"},
        {"name": "TOEIC", "id": "9afba032-ed69-4d5c-bc73-805ae6eb156b"},
        {"name": "STANAG German", "id": "6b381e55-528e-4d13-85a2-963f0710e962"},
        {"name": "ZDaF", "id": "3139c891-e59e-4345-9f87-e7e93b22d686"},
        {"name": "ZMF", "id": "e1bd3e67-363d-4e46-b616-89f22d64468f"},
        {"name": "KDS", "id": "2f682b71-a772-4b55-8d30-2100844f5b53"},
        {"name": "GDS", "id": "37147540-e3ac-49b8-8ae0-2121f417b92f"},
        {"name": "PNDS", "id": "22bc21ab-5a87-448e-a0f4-74d0136678df"},
        {"name": "DSH", "id": "62c41d70-2757-4378-a7c0-e90bdb57a051"},
        {"name": "STANAG French", "id": "9c615240-f23e-4b6b-abf6-b10327742a1f"},
        {"name": "DELF", "id": "b6cedca1-38c7-470c-8688-caab5a102aa8"},
        {"name": "DALF", "id": "c1177873-7ef0-4e59-b24c-803d430d7541"},
        {"name": "STANAG Spanish", "id": "62aeac61-0c0a-4962-af06-9b32c375ad0b"},
        {"name": "DELE", "id": "c6275399-7302-49ca-837d-811f9238a5dc"},
        {"name": "STANAG Italian", "id": "49d71536-e9fb-4110-8639-a07ca653e6fb"},
        {"name": "CILS", "id": "e1a2c256-8e11-4a94-8bfb-4d564c4a892f"},
        {"name": "STANAG Russian", "id": "43089ad0-722c-4f13-9a89-c809b2e3ecee"},
        {"name": "STANAG Polish", "id": "634fe5b9-8494-4586-b67a-191157c0ed60"},
        # vědecké
        # {'name': '', 'name_en': '', 'id': ''},
        # {'name': '', 'name_en': '', 'id': ''},
        # {'name': '', 'name_en': '', 'id': ''},
        # {'name': '', 'name_en': '', 'id': ''},
        # {'name': '', 'name_en': '', 'id': ''},
        # sportovní
        # {'name': '', 'name_en': '', 'id': ''},
        # {'name': '', 'name_en': '', 'id': ''},
        # {'name': '', 'name_en': '', 'id': ''},
        # {'name': '', 'name_en': '', 'id': ''},
        # {'name': '', 'name_en': '', 'id': ''},
        # pracovní
        # {'name': '', 'name_en': '', 'id': ''},
        # {'name': '', 'name_en': '', 'id': ''},
        # {'name': '', 'name_en': '', 'id': ''},
        # {'name': '', 'name_en': '', 'id': ''},
        # {'name': '', 'name_en': '', 'id': ''},
    ]
    return certificateTypes


def determineCertificateTypeGroup():
    certificateTypeGroups = [
        {
            "name": "jazykové",
            "name_en": "language",
            "id": "db9ba8c3-3d6e-4190-bfe7-d401586dd282",
        },
        {
            "name": "vědecké",
            "name_en": "science",
            "id": "bc988cb6-38a7-45a1-97ec-d1e220621355",
        },
        {
            "name": "sportovní",
            "name_en": "sport",
            "id": "3f1351ca-0624-43bb-9c93-23e6478fb1c1",
        },
        {
            "name": "pracovní",
            "name_en": "work",
            "id": "e4713dd6-69e6-4d35-964b-1bca141899eb",
        },
    ]
    return certificateTypeGroups


@cache
def determineMedalType():
    medalTypes = [
        # Řády a vyznamenání České republiky
        {"name": "Řád Bílého lva", "id": "cf4c274c-6cf1-11ed-a1eb-0242ac120002"},
        {
            "name": "Řád Tomáše Garrigua Masaryka",
            "id": "cf4c2ef4-6cf1-11ed-a1eb-0242ac120002",
        },
        {"name": "Medaile za hrdinství", "id": "cf4c3052-6cf1-11ed-a1eb-0242ac120002"},
        {"name": "Medaile za zásluhy", "id": "cf4c3188-6cf1-11ed-a1eb-0242ac120002"},
        # Vojenské resortní vyznamenání
        {"name": "Záslužný kříž", "id": "1ebfcc2a-6cf2-11ed-a1eb-0242ac120002"},
        {"name": "Medaile za zranění", "id": "1ebfcf2c-6cf2-11ed-a1eb-0242ac120002"},
        {
            "name": "Medaile ministra obrany za službu v zahraničí",
            "id": "1ebfd076-6cf2-11ed-a1eb-0242ac120002",
        },
        {
            "name": "Medaile Armády České republiky",
            "id": "1ebfd198-6cf2-11ed-a1eb-0242ac120002",
        },
        # Čestné odznaky
        {
            "name": "Čestný pamětní odznak za službu míru",
            "id": "97edb3fc-a4d2-4295-a8ca-e7e97fba87e1",
        },
        {
            "name": "Čestný pamětní odznak za službu v misi IFOR",
            "id": "159c84ce-3a57-423a-8e1b-c49ce19cd02a",
        },
        {
            "name": "Čestný pamětní odznak 50 let NATO",
            "id": "e8b157e2-30bf-4100-8449-60c9eea26018",
        },
        {
            "name": "Čestný pamětní odznak 10 let školícího a vzdělávacího střediska Ministerstva obrany Komorní Hrádek",
            "id": "62993164-aa76-4fcd-ab77-960f3b433e49",
        },
        {
            "name": "Pamětní odznak Summit NATO Praha 2002",
            "id": "9638bdbd-3fa4-4a5e-9295-e15fd57765c6",
        },
        {
            "name": "Pamětní odznak NATO 1999-2004",
            "id": "bc24e3df-5b18-4b19-933a-915b462f7d71",
        },
        {
            "name": "Pamětní medaile k 60. ukončení 2. světové války",
            "id": "6b3ea765-11e4-4ca0-9bbf-698c9d6d44d2",
        },
        {
            "name": "Pamětní odznak Vojenské akademie v Brně 1951-2004",
            "id": "11a8b0fd-f739-4293-9d8e-3f526aee2fc3",
        },
        {
            "name": "Čestný odznak Přemysla Otakara II., krále železného a zlatého",
            "id": "e1bbcb9b-91d3-498c-83ad-82dc168475d2",
        },
        {
            "name": "Pamětní odznak štábního kapitána Václava Morávka",
            "id": "dfa459de-63c4-4654-9eba-2c90bf1124c7",
        },
        {
            "name": 'Pamětní odznak 4. brigády rychlého nasazení "Obrany národa"',
            "id": "33fb8070-b5da-45f9-93a4-abceb1a54fd3",
        },
        {
            "name": "Čestný pamětní odznak k 50. výročí vzniku čs. výsadkového vojska",
            "id": "aa5f8d02-333b-45ee-9fc1-854fa3103b62",
        },
        {
            "name": "Čestný pamětní odznak za službu v misi SFOR",
            "id": "5e8ca930-4876-4360-ba3d-52ba1bb0b62e",
        },
        {
            "name": "Čestný pamětní odznak za službu v mírové misi na Balkáně",
            "id": "df5cfa34-66d6-47db-8714-24c7478490a8",
        },
        {
            "name": "Čestný pamětní odznak k 10. výročí války v Perském zálivu",
            "id": "d05662aa-3593-4ffc-bf7b-2d54b7ca336f",
        },
        {
            "name": "Pamětní odznak vojenské logistiky",
            "id": "a7dde577-8b5a-485d-8eea-f0f57512e49b",
        },
        {
            "name": "Pamětní odznak 4. průzkumného praporu Bechyně",
            "id": "6afa9a62-822f-4c89-91d7-573dbf089606",
        },
        {
            "name": "Čestný odznak generála JUDr. Viktora Spěváčka",
            "id": "32526f1a-8d94-4f62-b2d0-5564c9ff79b0",
        },
        {
            "name": "Pamětní odznak velitelství vzdušných sil",
            "id": "7d94ba3e-569d-461d-9a74-f969f259b35d",
        },
        {
            "name": "Pamětní odznak metrologie a technického dozoru",
            "id": "b532f548-2151-405c-83b1-04eb10678ced",
        },
        {
            "name": "Pamětní odznak Ústřední opravárenské základny automibilní techniky",
            "id": "3d6c001f-701e-4d7b-8a3d-86558b26b7b7",
        },
        {
            "name": "Pamětní odznak Ústřední opravárenské základny prostředků velení",
            "id": "2f90938f-9347-4e51-a3d6-8c8bb3b64501",
        },
        {
            "name": "Pamětní odznak Automobilního skladu Nový Jičín",
            "id": "c684f1d4-96df-49a3-bb96-a8220f5560ac",
        },
        {
            "name": "Pamětní odznak Vojenské akademie Vyškov",
            "id": "9f7c68ab-63e1-47a9-889e-6ef3ab13399b",
        },
        {
            "name": "Pamětní odznak Ústřední základny zbraní a zbraňových systémů",
            "id": "6ea03605-375f-48c1-a3b3-6430edda5f58",
        },
        {
            "name": "Pamětní odznak Ústřední opravárenské základny zbraní a zbraňových systémů",
            "id": "233e68ab-8f56-4b93-8b63-52b42da0c5d7",
        },
        {
            "name": "Pamětní odznak 7. polní nemocnice",
            "id": "d61eef29-8b1b-45b5-8ddc-1843cdcbaebd",
        },
        {
            "name": "Pamětní odznak Výcvikové základny mírových sil Český Krumlov",
            "id": "b682aa69-e877-4822-a473-b8e15f881f32",
        },
        {
            "name": "Pamětní odznak střediska Centre of Excellence",
            "id": "aa96f62f-2836-449d-a48a-a873425ba80f",
        },
        {
            "name": "Pamětní odznak Vojenské policie - Irák",
            "id": "05d7c18f-649e-483b-9e26-0c055528aca5",
        },
        {
            "name": "Pamětní odznak Střední technické školy",
            "id": "972b27d9-1e11-424e-bdd3-4f08f48c555c",
        },
        {
            "name": "Pamětní odznak 5. dopravní základny logistické a zdravotnické podpory",
            "id": "1dbaddb5-07f6-4bc4-922e-2d444e945ee9",
        },
        {
            "name": "Pamětní odznak Výzkumného střediska Doksy",
            "id": "a482970b-f29d-4de7-a71a-abdcd403c87e",
        },
        {
            "name": "Pamětní odznak Speciálních sil mise Enduring Freedom z Afghánistánu",
            "id": "2301eb86-2d8d-4da1-9ad3-78d9b5b5871b",
        },
        {
            "name": "Pamětní odznak Vojenské lékařské akademie J. E. Purkyně",
            "id": "96ddedbb-d4e8-411b-8773-8f1adda1782b",
        },
        {
            "name": "Pamětní odznak Ústřední základny materiálu všeobecného použití",
            "id": "fa838268-8a26-46fc-b36d-a8032ac4e682",
        },
        {
            "name": "Pamětní odznak 2. mechnizované brigády Písek",
            "id": "c5c2d05b-1977-4ff2-b027-218a703c57d9",
        },
        {
            "name": "Pamětní odznak Letecké opravárenské základny Brno",
            "id": "7b751e5f-bc44-4a04-847b-3b776dd2d298",
        },
        {
            "name": "Pamětní odznak 601. skupiny speciálních sil",
            "id": "93b8b1af-d91f-4676-ac75-d374c8dc78a1",
        },
        {
            "name": "Pamětní odznak Ústřední opravárenské základny materiálu osobního použití Chrudim",
            "id": "bbbef578-0a80-4c81-a56b-a7b7ec6576f2",
        },
        {"name": "Pamětní odznak KFOR", "id": "efb084a0-7a87-464e-8ecd-7596fb9337c9"},
        {
            "name": "Pamětní odznak veterinární základny Grabštejn",
            "id": "bf8af41c-ef71-43cb-9a69-fc7e01efccf7",
        },
        {
            "name": "Pamětní odznak 51. NPP Pardubice",
            "id": "fa11b6df-8f45-4f00-80f5-22805108113b",
        },
        {
            "name": "Pamětní odznak 7. mechanizované brigády „Dukelské“ Hranice",
            "id": "e0bbb6f3-341c-450c-ac33-f4662eac270c",
        },
        {
            "name": "Pamětní odznak Hradní stráže",
            "id": "752bb4ee-f9ac-446d-bbb8-2592ce3ade79",
        },
        {
            "name": "Pamětní odznak Inspekce MO a bývalého ÚřK BVLSI",
            "id": "0f682be0-bb44-40fd-85b6-8eed606ca329",
        },
        {
            "name": "Pamětní odznak pro 312. prapor chemické ochrany NATO za službu v jednotkách NRF",
            "id": "fbc8a9e0-8695-4a06-93ad-915065b04d91",
        },
        {
            "name": "Pamětní odznak Vojenské střední školy Vyškov",
            "id": "36e1bc46-472c-4d43-b272-1fb994d581c6",
        },
    ]
    return medalTypes


@cache
def determineMedalTypeGroup():
    medalTypeGroup = [
        {
            "name": "Řády a vyznamenání České republiky",
            "id": "0747704c-d6f9-461c-9b2f-4b9681bd50ed",
        },
        {
            "name": "Vojenské resortní vyznamenání",
            "id": "2c34f055-d2fa-4eb1-a29a-ed28a2277e6c",
        },
        {"name": "Čestné odznaky", "id": "6299630e-4d27-44a9-a844-53831add33ca"},
    ]
    return medalTypeGroup


@cache
def determineWorkHistoryPosition():
    workHistoryPosition = [
        {"name": "manažer", "id": "3406c765-8454-4f3a-b3bb-76b74582be2e"},
        {"name": "účetní", "id": "d9a50a22-edf4-4264-98f0-5a9eced115c4"},
        {"name": "úředník", "id": "203cb4d1-6d61-4dfd-8662-d7a352db739c"},
        {"name": "konzultant", "id": "7925ca15-acd5-4af9-9731-2884c8225081"},
        {"name": "asistent", "id": "fd8ea6b7-4706-4537-8569-5dc8040519f8"},
        {"name": "právní zástupce", "id": "242a84a8-f754-4136-b322-e20b0382dff4"},
        {"name": "administrátor", "id": "cc3f7106-f38c-48ee-89d9-d1a420e45df5"},
        {"name": "pokladní", "id": "950d3466-af5b-4a59-b91f-14514bf693d0"},
        {"name": "uklízeč", "id": "c24dba24-b636-46d4-b0b2-2dc03e6af933"},
        {"name": "operátor", "id": "02addd4f-ee6f-4141-bbc7-5a6ca9bc8647"},
        {"name": "analytik", "id": "aaea9b89-dbed-42a2-8f22-737ce913f803"},
        {"name": "správce", "id": "87897e28-c92d-49be-8878-e9c39c9b8a5a"},
        {"name": "technická podpora", "id": "f60e38af-069b-4f8e-8cc9-b6cd077a7cee"},
        {"name": "řidič", "id": "c11f1606-bdd2-4973-89ca-1489e8249c0f"},
        {"name": "specialista", "id": "8b18a1a2-f759-4441-a18b-0bee41e71519"},
    ]
    return workHistoryPosition


# from gql_personalities.DBDefinitions import

import asyncio

import os
import json
from uoishelpers.feeders import ImportModels
import datetime

def get_demodata():
    def datetime_parser(json_dict):
        for (key, value) in json_dict.items():
            if key in ["startdate", "enddate", "lastchange", "created"]:
                dateValue = datetime.datetime.fromisoformat(value)
                dateValueWOtzinfo = dateValue.replace(tzinfo=None)
                json_dict[key] = dateValueWOtzinfo
        return json_dict


    with open("./systemdata.json", "r") as f:
        jsonData = json.load(f, object_hook=datetime_parser)

    return jsonData

async def initDB(asyncSessionMaker):

    defaultNoDemo = "False"
    if defaultNoDemo == os.environ.get("DEMO", defaultNoDemo):
        dbModels = [
            CertificateTypeGroupModel,
            CertificateTypeModel, 
            MedalTypeGroupModel,
            MedalTypeModel, 
            RankTypeModel, 
        ]
    else:
        dbModels = [
            CertificateTypeGroupModel,
            CertificateTypeModel, 
            MedalTypeGroupModel,
            MedalTypeModel, 
            RankTypeModel, 

            RankModel,
            StudyModel,
            CertificateModel,
            MedalModel,
            WorkHistoryModel,
            RelatedDocModel
        ]

    jsonData = get_demodata()
    await ImportModels(asyncSessionMaker, dbModels, jsonData)
    pass