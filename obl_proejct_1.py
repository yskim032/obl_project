import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
import json
from typing import List, Dict
from tkinterdnd2 import DND_FILES, TkinterDnD
from datetime import datetime

# pyinstaller -w -F --add-binary="C:/Users/kod03/AppData/Local/Programs/Python/Python311/tcl/tkdnd2.8;tkdnd2.8" example.py

class ContainerConverter:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.title("CLL to OBL Converter")
        self.root.geometry("1000x900")  # 창 크기 증가

        # 설정 파일 경로 설정
        self.config_dir = os.path.join(os.path.expanduser("~"), "Desktop", "OBL_Configs")
        os.makedirs(self.config_dir, exist_ok=True)
        
        self.stowage_config_file = os.path.join(self.config_dir, "stowage_mapping.json")
        self.port_config_file = os.path.join(self.config_dir, "port_mapping.json")
        self.tpsz_config_file = os.path.join(self.config_dir, "tpsz_mapping.json")
        
        # 매핑 설정 로드
        self.stowage_settings = self.load_stowage_settings()
        self.stow_mapping = self.stowage_settings.get('mapping', {})
        self.stow_column_mapping = self.stowage_settings.get('column_mapping', {
            'discharge_port': 'FPOD',
            'stowage_code': 'Stow'
        })
        
        # TpSz 매핑 설정 로드
        self.tpsz_settings = self.load_tpsz_settings()
        self.tpsz_mapping = self.tpsz_settings.get('mapping', {})
        self.tpsz_column_mapping = self.tpsz_settings.get('column_mapping', {
            'before': 'Description',
            'after': 'Code'
        })
        
        # PORT CODE 매핑 추가
        self.port_codes = {'AEAJM': 'AJMAN', 'AEAUH': 'ABU DHABI', 'AEDXB': 'DUBAI', 'AEFJR': 'AL - FUJAYRAH', 'AEJEA': 'JEBEL ALI', 'AEKLF': 'KHOR AL FAKKAN', 'AEPRA': 'PORT RASHID', 'AEQIW': 'UMM AL QAIWAIN', 'AERKT': 'RAS AL KHAIMAH', 'AESHJ': 'SHARJAH', 'AEYAS': 'YAS ISLAND', 'AGANU': 'ANTIGUA', 'AIRBY': 'ROAD BAY', 'ALDRZ': 'DURRES', 'ALSAR': 'SARANDE', 'AOLAD': 'LUANDA', 'AOLOB': 'LOBITO', 'AOMSZ': 'NAMIBE', 'ARBHI': 'BAHIA BLANCA', 'ARBUE': 'BUENOS AIRES', 'ARCMP': 'CAMPANA', 'ARCNQ': 'CORRIENTES', 'ARLPG': 'LA PLATA', 'ARMDQ': 'MAR DEL PLATA', 'ARPMY': 'PUERTO MADRYN', 'ARPSS': 'POSADAS', 'ARROS': 'ROSARIO', 'ARSAE': 'SAN ANTONIO ESTE', 'ARUSH': 'USHUAIA', 'ARZAE': 'ZARATE', 'ASPPG': 'PAGO PAGO', 'AUABP': 'ABBOT POINT', 'AUADL': 'ADELAIDE', 'AUALH': 'ALBANY', 'AUBEL': 'BELL BAY', 'AUBNE': 'BRISBANE', 'AUBOO': 'BOOBY ISLAND', 'AUCNS': 'CAIRNS', 'AUDRW': 'DARWIN', 'AUEPR': 'ESPERANCE', 'AUFRE': 'FREMANTLE', 'AUGLT': 'GLADSTONE', 'AUHBA': 'HOBART', 'AUHPT': 'HAY POINT', 'AUMEL': 'MELBOURNE', 'AUNTL': 'NEWCASTLE', 'AUPHE': 'PORT HEDLAND', 'AUPKL': 'PORT KEMBLA', 'AUSYD': 'SYDNEY', 'AWORJ': 'ORANJESTAD', 'BBBGI': 'BRIDGETOWN', 'BDCGP': 'CHATTOGRAM', 'BDMGL': 'MONGLA', 'BEANR': 'ANTWERP', 'BEGNE': 'GENT (GHENT)', 'BEZEE': 'ZEEBRUGGE', 'BGBOJ': 'BURGAS', 'BGVAR': 'VARNA', 'BHKBS': 'BAHRAIN', 'BJCOO': 'COTONOU', 'BMBDA': 'HAMILTON', 'BMKWF': 'KINGS WHARF', 'BNMUA': 'MUARA', 'BQEUX': 'SINT EUSTATIUS', 'BRACB': 'ARRAIAL DO CABO', 'BRADR': 'ANGRA DOS REIS', 'BRANG': 'ARTUR NOGUEIRA', 'BRBEL': 'BELEM', 'BRBZC': 'BUZIOS', 'BRCBU': 'CAMBORIU', 'BRCDO': 'CABEDELO', 'BRCOP': 'CARMO DO PARANAIBA', 'BRFOR': 'FORTALEZA', 'BRIBB': 'IMBITUBA', 'BRIBE': 'ILHABELA', 'BRIGE': 'ILHA GRANDE', 'BRIGI': 'ITAGUAI', 'BRIOA': 'ITAPOA', 'BRIOS': 'ILHEUS', 'BRIQI': 'ITAQUI', 'BRITA': 'ITACOATIARA', 'BRITJ': 'ITAJAI', 'BRMAO': 'MANAUS', 'BRMCZ': 'MACEIO', 'BRNVT': 'NAVEGANTES', 'BRPBO': 'PORTO BELO', 'BRPEC': 'PECEM', 'BRPNG': 'PARANAGUA', 'BRPVH': 'PORTO VELHO', 'BRQCK': 'CABO FRIO', 'BRREC': 'RECIFE', 'BRRIG': 'RIO GRANDE', 'BRRIO': 'RIO DE JANEIRO', 'BRSFS': 'SAO FRANCISCO DO SUL', 'BRSSA': 'SALVADOR', 'BRSSZ': 'SANTOS', 'BRSTM': 'SANTAREM', 'BRSUA': 'SUAPE', 'BRUBT': 'UBATUBA', 'BRVIX': 'VITORIA', 'BRVLC': 'VILA DO CONDE', 'BSCOC': 'COCO CAY', 'BSFPO': 'FREEPORT, GRAND BAHAMA', 'BSGSC': 'GREAT STIRRUP CAY', 'BSHMC': 'LITTLE SAN SALVADOR', 'BSLUC': 'LUCAYA', 'BSNAS': 'NASSAU', 'BZBZE': 'BELIZE CITY', 'CABCO': 'BAIE COMEAU', 'CABEC': 'BECANCOUR', 'CACBK': 'CORNER BROOK', 'CACHA': 'CHARLOTTETOWN', 'CAGPE': 'GASPE', 'CAHAL': 'HALIFAX', 'CAHSP': 'HAVRE-SAINT-PIERRE', 'CALBA': 'LA BAIE', 'CAMTR': 'MONTREAL', 'CAPRR': 'PRINCE RUPERT', 'CAQUE': 'QUEBEC', 'CASJB': 'SAINT JOHN', 'CASYD': 'SYDNEY', 'CATRR': 'TROIS-RIVIERES (THREE RIVERS)', 'CAVAN': 'VANCOUVER', 'CCCCK': 'COCOS ISLANDS', 'CDMAT': 'MATADI', 'CGPNR': 'POINTE NOIRE', 'CIABJ': 'ABIDJAN', 'CISPY': 'SAN-PEDRO', 'CKAIT': 'AITUTAKI', 'CKRAR': 'RAROTONGA', 'CLANF': 'ANTOFAGASTA', 'CLARI': 'ARICA', 'CLCNL': 'CORONEL', 'CLCQQ': 'COQUIMBO', 'CLIPC': 'ISLA DE PASCUA', 'CLIQQ': 'IQUIQUE', 'CLLQN': 'LIRQUEN', 'CLPAG': 'PUERTO ANGAMOS', 'CLPPY': 'MAGELLAN STRAIT', 'CLSAI': 'SAN ANTONIO', 'CLSVE': 'SAN VICENTE', 'CLVAP': 'VALPARAISO', 'CMDLA': 'DOUALA', 'CMKBI': 'KRIBI', 'CNBHT': 'TIESHAN', 'CNCAN': 'GUANGZHOU', 'CNCFD': 'CAOFEIDIAN', 'CNDCB': 'DA CHAN BAY', 'CNDLC': 'DALIAN', 'CNFAN': 'FANGCHENG', 'CNFOC': 'FUZHOU', 'CNHAK': 'HAIKOU', 'CNHNH': 'HUANGHUA', 'CNHUA': 'HUANGPU', 'CNJIA': 'JIANGYIN', 'CNJIN': 'JINGTANG (TANGSHAN)', 'CNLUH': 'LU-HUA SHAN', 'CNLYG': 'LIANYUNGANG', 'CNMAW': 'MAWEI', 'CNMWN': 'MAWAN', 'CNNGB': 'NINGBO', 'CNNKG': 'NANJING', 'CNNSA': 'NANSHA', 'CNNTG': 'NANTONG', 'CNQZH': 'QINZHOU', 'CNRZH': 'RIZHAO', 'CNSHA': 'SHANGHAI', 'CNSHG': 'SANSHAN', 'CNSHK': 'SHEKOU', 'CNSHP': 'QINHUANGDAO', 'CNSWA': 'SHANTOU', 'CNSYX': 'SANYA', 'CNTAG': 'TAICANG', 'CNTAO': 'QINGDAO', 'CNTSI': 'JINGJIANG', 'CNTXG': 'TIANJINXINGANG', 'CNWEF': 'WEIFANG', 'CNWEI': 'WEIHAI', 'CNXMN': 'XIAMEN', 'CNXSI': 'XIANGSHUI', 'CNYNT': 'YANTAI', 'CNYTN': 'YANTIAN', 'CNZJG': 'ZHANGJIAGANG', 'CNZOS': 'ZHOUSHAN', 'COBAQ': 'BARRANQUILLA', 'COBUN': 'BUENAVENTURA', 'COCTG': 'CARTAGENA', 'COSMR': 'SANTA MARTA', 'COTRB': 'TURBO', 'CRCAL': 'CALDERA', 'CRLIO': 'PUERTO LIMON', 'CRMOB': 'MOIN', 'CUGER': 'NUEVA GERONA', 'CUHAV': 'LA HABANA', 'CUMAR': 'MARIEL', 'CVMIN': 'MINDELO', 'CVRAI': 'PRAIA', 'CWCUR': 'CURACAO', 'CYFMG': 'FAMAGUSTA', 'CYLMS': 'LIMASSOL', 'DEBRB': 'BRUNSBUTTEL', 'DEBRE': 'BREMEN', 'DEBRV': 'BREMERHAVEN', 'DEELS': 'ELSFLETH', 'DEEME': 'EMDEN', 'DEHAM': 'HAMBURG', 'DEHGL': 'HELGOLAND', 'DEKEL': 'KIEL', 'DELBC': 'LUBECK', 'DEWAR': 'WARNEMUNDE', 'DEWVN': 'WILHELMSHAVEN', 'DJJIB': 'DJIBOUTI', 'DKAAL': 'AALBORG', 'DKAAR': 'AARHUS', 'DKCPH': 'COPENHAGEN', 'DKFRC': 'FREDERICIA', 'DKGBT': 'GREAT BELT', 'DKHVS': 'HVIDE SANDE', 'DKKAL': 'KALUNDBORG', 'DKKLD': 'KOLIND', 'DKKTD': 'KERTEMINDE', 'DKODE': 'ODENSE', 'DKRNN': 'RONNE', 'DKSKA': 'SKAGEN', 'DMPOR': 'PORTSMOUTH', 'DMRSU': 'ROSEAU', 'DOCAU': 'CAUCEDO', 'DOHAI': 'RIO HAINA', 'DOPOP': 'PUERTO PLATA', 'DZAAE': 'ANNABA', 'DZALG': 'ALGER', 'DZAZW': 'ARZEW', 'DZBJA': 'BEJAIA', 'DZDJE': 'DJEN-DJEN', 'DZGHZ': 'GHAZAOUET', 'DZORN': 'ORAN', 'DZSKI': 'SKIKDA', 'ECESM': 'ESMERALDAS', 'ECGYE': 'GUAYAQUIL', 'ECLLD': 'LA LIBERTAD', 'ECPBO': 'PUERTO BOLIVAR', 'ECPSJ': 'POSORJA', 'EETLL': 'TALLINN', 'EGAKI': 'ABU KIR', 'EGALY': 'ALEXANDRIA OLD PORT', 'EGDAM': 'DAMIETTA', 'EGEDK': 'ALEXANDRIA EL DEKHEILA', 'EGPSE': 'PORT SAID EAST', 'EGPSW': 'PORT SAID WEST', 'EGSGA': 'SAFAGA', 'EGSOK': 'SOKHNA PORT', 'EGSSH': 'SHARM ASH SHAYKH', 'EGSUZ': 'SUEZ', 'ERASA': 'ASSAB', 'ESACE': 'ARRECIFE DE LANZAROTE', 'ESAGP': 'MALAGA', 'ESALC': 'ALICANTE', 'ESALG': 'ALGECIRAS', 'ESALM': 'ALMAGRO', 'ESBCN': 'BARCELONA', 'ESBIO': 'BILBAO', 'ESCAD': 'CADIZ', 'ESCAR': 'CARTAGENA', 'ESCAS': 'CASTELLON DE LA PLANA', 'ESCEU': 'CEUTA', 'ESFRO': 'FERROL', 'ESFUE': 'PUERTO DEL ROSARIO-FUERTEVENTURA', 'ESGIJ': 'GIJON', 'ESGJI': 'GRANJA DE SAN IDELFONSO', 'ESHUV': 'HUELVA', 'ESIBZ': 'IBIZA', 'ESLCG': 'LA CORUNA', 'ESLEI': 'ALMERIA', 'ESLPA': 'LAS PALMAS', 'ESMAH': 'MAHON, MENORCA', 'ESMPG': 'MARIN, PONTEVEDRA', 'ESPAL': 'PALAMOS', 'ESPMI': 'PALMA DE MALLORCA', 'ESROS': 'ROSAS', 'ESSAG': 'SAGUNTO', 'ESSCT': 'SANTA CRUZ DE TENERIFE', 'ESSPC': 'SANTA CRUZ DE LA PALMA', 'ESSSG': 'SAN SEBASTIAN DE LA GOMERA', 'ESSVQ': 'SEVILLA', 'ESTAR': 'TARRAGONA', 'ESVGO': 'VIGO', 'ESVLC': 'VALENCIA', 'FIHEL': 'HELSINKI', 'FIKEM': 'KEMI', 'FIKOK': 'KOKKOLA (KARLEBY)', 'FIKTK': 'KOTKA', 'FIOUL': 'OULU (ULEABORG)', 'FIRAU': 'RAUMA', 'FITOR': 'TORNIO (TORNEA)', 'FJLTK': 'LAUTOKA', 'FJSUV': 'SUVA', 'FOTHO': 'THORSHAVN', 'FRAJA': 'AJACCIO', 'FRBES': 'BREST', 'FRBOD': 'BORDEAUX', 'FRCEQ': 'CANNES', 'FRCER': 'CHERBOURG', 'FRDKK': 'DUNKERQUE', 'FRFOS': 'FOS-SUR-MER', 'FRGVL': 'GENNEVILLIERS', 'FRHON': 'HONFLEUR', 'FRLEH': 'LE HAVRE', 'FRLRH': 'LA ROCHELLE', 'FRLVE': 'LE VERDON', 'FRMRS': 'MARSEILLE', 'FRMTX': 'MONTOIR-DE-BRETAGNE', 'FRNCE': 'NICE', 'FRSET': 'SETE', 'FRSFP': 'SIX-FOURS-LES-PLAGES', 'FRSNR': 'ST NAZAIRE', 'FRSTM': 'ST MARCEL', 'FRSTP': 'ST TROPEZ', 'FRTLN': 'TOULON', 'FRURO': 'ROUEN', 'FRVFM': 'VILLEFRANCHE-SUR-MER', 'GALBV': 'LIBREVILLE', 'GAPOG': 'PORT GENTIL', 'GBBEL': 'BELFAST', 'GBBRS': 'BRISTOL', 'GBDVR': 'DOVER', 'GBFAL': 'FALMOUTH', 'GBFXT': 'FELIXSTOWE', 'GBGRG': 'GRANGEMOUTH', 'GBGRK': 'GREENOCK', 'GBHRW': 'HARWICH', 'GBIMM': 'IMMINGHAM', 'GBLER': 'LERWICK', 'GBLGP': 'LONDON GATEWAY PORT', 'GBLIV': 'LIVERPOOL', 'GBNCS': 'NEWCASTLE', 'GBPME': 'PORTSMOUTH', 'GBPRT': 'PORTREE', 'GBPRU': 'PORTBURY', 'GBPTL': 'PORTLAND', 'GBSOQ': 'SOUTH QUEENSFERRY', 'GBSOU': 'SOUTHAMPTON', 'GBSSH': 'SOUTH SHIELDS', 'GBTEE': 'TEESPORT', 'GBTHP': 'THAMESPORT', 'GBTIL': 'TILBURY', 'GDGND': 'GRENADA', 'GDSTG': "SAINT GEORGE'S", 'GEBUS': 'BATUMI', 'GEPTI': 'POTI', 'GGSPT': 'ST PETER PORT', 'GHTEM': 'TEMA', 'GHTKD': 'TAKORADI', 'GIGIB': 'GIBRALTAR', 'GLGOH': 'NUUK (GODTHAAB)', 'GLJFR': 'PAAMIUT (FREDRIKSHAAB)', 'GMBJL': 'BANJUL', 'GNCKY': 'CONAKRY', 'GPPTP': 'POINTE-A-PITRE', 'GRARM': 'ARGOSTOLION', 'GRCFU': 'KERKIRA (CORFU)', 'GRCHQ': 'CANEA (CHANIA)', 'GRELE': 'ELEFSIS (ELEVSIS)', 'GRGYT': 'GYTHION', 'GRHER': 'HERAKLION', 'GRJMK': 'MYKONOS', 'GRJSY': 'SYROS (SYRA)', 'GRJTR': 'THIRA', 'GRKAK': 'KATAKOLON', 'GRKGS': 'KOS', 'GRKLL': 'KALILIMENES', 'GRKLX': 'KALAMATA', 'GRLAV': 'LAURIUM (LAVRION)', 'GRMDR': 'MOUDHROS', 'GRMON': 'MONEMVASIA', 'GRNAF': 'NAFPLION', 'GRPIR': 'PIRAEUS', 'GRPMS': 'PATMOS', 'GRRHO': 'RHODES', 'GRSDH': 'SOUDA', 'GRSKA': 'SKARAMANGAS', 'GRSKG': 'THESSALONIKI', 'GRTIL': 'TILOS', 'GRVOL': 'VOLOS', 'GRZTH': 'ZAKYNTHOS', 'GTPBR': 'PUERTO BARRIOS', 'GTPRQ': 'PUERTO QUETZAL', 'GTSTC': 'PUERTO SANTO TOMAS DE CASTILLA', 'GWOXB': 'BISSAU', 'GYGEO': 'GEORGETOWN', 'HKHKG': 'HONG KONG', 'HNPCA': 'PUERTO CASTILLA', 'HNPCR': 'PUERTO CORTES', 'HNRTB': 'ROATAN', 'HNSLO': 'SAN LORENZO', 'HRDBV': 'DUBROVNIK', 'HRPLE': 'PLOCE', 'HRRJK': 'RIJEKA', 'HRSPU': 'SPLIT', 'HRZAD': 'ZADAR', 'HTGVS': 'GONAIVES', 'HTLAB': 'LABADIE', 'HTPAP': 'PORT AU PRINCE', 'IDBDJ': 'BANJARMASIN', 'IDBLW': 'BELAWAN, SUMATRA', 'IDBOA': 'BENOA, BALI', 'IDBPN': 'BALIKPAPAN, KALIMANTAN', 'IDBTM': 'BATAM ISLAND', 'IDDJB': 'JAMBI, SUMATRA', 'IDJKT': 'JAKARTA, JAVA', 'IDMAK': 'MAKASSAR', 'IDMAL': 'MANGOLE', 'IDPDG': 'PADANG', 'IDPER': 'PERAWANG', 'IDPLM': 'PALEMBANG, SUMATRA', 'IDPNJ': 'PANJANG', 'IDPNK': 'PONTIANAK, KALIMANTAN', 'IDPWG': 'PERAWANG, SUMATRA', 'IDSRG': 'SEMARANG', 'IDSUB': 'SURABAYA', 'IDTAB': 'TABONEO', 'IDTBA': 'TANJUNG BARA, KL', 'IDUPG': 'UJUNG PANDANG, SULAWESI', 'IEDLG': 'DUN LAOGHAIRE', 'IEDUB': 'DUBLIN', 'IEGRE': 'GREENCASTLE', 'IEORK': 'CORK', 'IEWAT': 'WATERFORD', 'ILASH': 'ASHDOD', 'ILETH': 'ELAT (EILATH)', 'ILHFA': 'HAIFA', 'INALA': 'ALANG SBY', 'INBHU': 'BHAVNAGAR', 'INBOM': 'MUMBAI', 'INCCU': 'KOLKATA', 'INCOK': 'COCHIN', 'INENR': 'ENNORE', 'INGGV': 'GANGAVARAM', 'INHAL': 'HALDIA', 'INHZA': 'HAZIRA PORT/SURAT', 'INIXY': 'KANDLA', 'INJGD': 'JAIGAD', 'INKAK': 'KAKINADA', 'INKAT': 'KATTUPALLI', 'INKRI': 'KRISHNAPATNAM', 'INMAA': 'CHENNAI', 'INMRM': 'MARMUGAO (MARMAGAO)', 'INMUN': 'MUNDRA', 'INNML': 'NEW MANGALORE', 'INNSA': 'NHAVA SHEVA', 'INNYY': '(OLD) VIZHINJAM INTERNATIONAL SEA PORT', 'INPAV': 'PIPAVAV (VICTOR) PORT', 'INPRT': 'PARADIP GARH', 'INTRV': 'VIZHINJAM INTERNATIONAL SEA PORT', 'INTUN': 'TUNA', 'INTUT': 'TUTICORIN', 'INVTZ': 'VISAKHAPATNAM', 'IQUQR': 'UMM QASR PT', 'ISAKU': 'AKUREYRI', 'ISISA': 'ISAFJORDUR - HOFN', 'ISREY': 'REYKJAVIK', 'ITAHO': 'ALGHERO', 'ITAOI': 'ANCONA', 'ITAUG': 'AUGUSTA PORT OF CATANIA', 'ITBDS': 'BRINDISI', 'ITBRI': 'BARI', 'ITCAG': 'CAGLIARI', 'ITCTA': 'CATANIA', 'ITCVV': 'CIVITAVECCHIA', 'ITGIT': 'GIOIA TAURO', 'ITGOA': 'GENOA', 'ITISS': 'ISOLA SANTO STEFANO', 'ITLIV': 'LEGHORN', 'ITMNF': 'MONFALCONE', 'ITMSN': 'MESSINA', 'ITNAP': 'NAPLES', 'ITOLB': 'OLBIA', 'ITPAL': 'PALAZZOLO DELLO STELLA', 'ITPMA': 'MARGHERA', 'ITPMO': 'PALERMO', 'ITPPL': 'PORTOPALO', 'ITPTF': 'PORTOFINO', 'ITPZL': 'POZZALLO', 'ITQSS': 'SASSARI', 'ITRAN': 'RAVENNA', 'ITRRO': 'SORRENTO', 'ITSAL': 'SALERNO', 'ITSIR': 'SIRACUSA', 'ITSPE': 'LA SPEZIA', 'ITSVN': 'SAVONA', 'ITTAR': 'TARANTO', 'ITTPS': 'TRAPANI', 'ITTRS': 'TRIESTE', 'ITVCE': 'VENICE', 'ITVDL': 'VADO LIGURE', 'JMFMH': 'FALMOUTH', 'JMKIN': 'KINGSTON', 'JMMBJ': 'MONTEGO BAY', 'JMOCJ': 'OCHO RIOS', 'JOAQJ': "AL 'AQABAH", 'JPABU': 'ABURATSU', 'JPAOJ': 'AOMORI', 'JPAXT': 'AKITA', 'JPBEP': 'BEPPU, SHIMANE', 'JPCHB': 'CHIBA', 'JPFKY': 'FUKUYAMA, HIROSHIMA', 'JPFUK': 'FUKUOKA', 'JPHBK': 'HIBIKISHINKO', 'JPHHE': 'HACHINOHE, AOMORI', 'JPHIC': 'HITACHINAKA', 'JPHIJ': 'HIROSHIMA', 'JPHIM': 'HIMEJI', 'JPHKD': 'HAKODATE', 'JPHKT': 'HAKATA, FUKUOKA', 'JPHMD': 'HAMADA', 'JPHSM': 'HOSOSHIMA', 'JPIMB': 'IMABARI', 'JPIMI': 'IMARI', 'JPISI': 'ISHIKARI', 'JPIWK': 'IWAKUNI', 'JPIYM': 'IYOMISHIMA', 'JPKCZ': 'KOCHI', 'JPKIJ': 'NIIGATA', 'JPKIS': 'KAMAISHI', 'JPKMJ': 'KUMAMOTO', 'JPKNZ': 'KANAZAWA', 'JPKOJ': 'KAGOSHIMA', 'JPKRE': 'KURE, HIROSHIMA', 'JPKSM': 'KASHIMA, IBARAKI', 'JPKUH': 'KUSHIRO', 'JPKWS': 'KAWASAKI', 'JPMAI': 'MAIZURU', 'JPMII': 'MIIKE, FUKUOKA', 'JPMIZ': 'MIZUSHIMA', 'JPMOJ': 'MOJI/KITAKYUSHU', 'JPMUR': 'MURORAN', 'JPMYJ': 'MATSUYAMA', 'JPMYK': 'MIYAKO, IWATE', 'JPNAH': 'NAHA, OKINAWA', 'JPNAN': 'NAKANOSEKI', 'JPNAO': 'NAOETSU', 'JPNGO': 'NAGOYA', 'JPNGS': 'NAGASAKI', 'JPOFT': 'OHFUNATO', 'JPOIT': 'OITA', 'JPOMZ': 'OMAEZAKI', 'JPONA': 'ONAHAMA', 'JPOSA': 'OSAKA', 'JPOTK': 'OTAKE', 'JPSBS': 'SHIBUSHI', 'JPSDJ': 'SENDAI, MIYAGI', 'JPSHS': 'SHIMONOSEKI', 'JPSKT': 'SAKATA', 'JPSMN': 'SAKAIMINATO', 'JPSMZ': 'SHIMIZU', 'JPSTS': 'SATSUMASENDAI', 'JPTAK': 'TAKAMATSU', 'JPTHS': 'TOYOHASHI', 'JPTKS': 'TOKUSHIMA', 'JPTKY': 'TOKUYAMA', 'JPTMK': 'TOMAKOMAI', 'JPTOS': 'TOYAMASHINKO', 'JPTRG': 'TSURUGA', 'JPTYO': 'TOKYO', 'JPUBJ': 'UBE', 'JPUKB': 'KOBE', 'JPWAK': 'WAKAYAMA', 'JPYAT': 'YATSUSHIRO', 'JPYKK': 'YOKKAICHI', 'JPYOK': 'YOKOHAMA', 'KEEMB': 'EMBAKASI', 'KEMBA': 'MOMBASA', 'KHKOS': 'KAMPONG SAOM (SIHANOUKVILLE)', 'KHPNH': 'PHNOM PENH', 'KMMUT': 'MUTSAMUDU', 'KMYVA': 'MORONI', 'KNBAS': 'BASSETERRE, ST KITTS', 'KNNEV': 'NEVIS', 'KRGSO': 'GOSEONG-GUN', 'KRINC': 'INCHEON', 'KRKAG': 'GANGNEUNG', 'KRKAN': 'GWANGYANG', 'KRKPO': 'POHANG', 'KRMOK': 'MOKPO', 'KROKP': 'OKPO/GEOJE', 'KRPTK': 'PYEONGTAEK', 'KRPUS': 'BUSAN', 'KRSCP': 'SAMCHEONPO/SACHEON', 'KRSPO': 'SEOGWIPO', 'KRTJI': 'DANGJIN', 'KRTYG': 'TONGYEONG', 'KRUSN': 'ULSAN', 'KRYOS': 'YEOSU', 'KWSAA': 'SHUAIBA', 'KWSWK': 'SHUWAIKH', 'KZALA': 'ALMATY', 'LBBEY': 'BEIRUT', 'LCCAS': 'CASTRIES', 'LCSLU': 'ST LUCIA APT', 'LKCMB': 'COLOMBO', 'LKGAL': 'GALLE', 'LKHBA': 'HAMBANTOTA', 'LKTRR': 'TRINCOMALEE', 'LRMLW': 'MONROVIA', 'LTKLJ': 'KLAIPEDA', 'LVRIX': 'RIGA', 'LYBEN': 'BINGAZI', 'LYKHO': 'KHOMS', 'LYMRA': 'MISURATA', 'LYTIP': 'TRIPOLI', 'MAAGA': 'AGADIR', 'MACAS': 'CASABLANCA', 'MANDR': 'NADOR', 'MAPTM': 'TANGER MED', 'MCMCM': 'MONTE-CARLO', 'MDGIU': 'GIURGIULESTI', 'MEBAR': 'BAR', 'MEBIJ': 'BIJELA', 'MEKOT': 'KOTOR', 'MGDIE': 'DIEGO SUAREZ', 'MGEHL': 'EHOALA (TOLAGNARO)', 'MGFTU': 'FORT DAUPHIN (TOALAGNARO)', 'MGMJN': 'MAJUNGA', 'MGNOS': 'NOSY-BE', 'MGSMS': 'SAINTE MARIE', 'MGTLE': 'TULEAR', 'MGTMM': 'TAMATAVE', 'MGVOH': 'VOHEMAR', 'MGWVK': 'MANAKARA', 'MMRGN': 'YANGON', 'MOMFM': 'MACAU', 'MQFDF': 'FORT-DE-FRANCE', 'MRNDB': 'NOUADHIBOU', 'MRNKC': 'NOUAKCHOTT', 'MSLTB': 'LITTLE BAY', 'MSPLY': 'PLYMOUTH', 'MTMAR': 'MARSAXLOKK', 'MTMLA': 'VALLETTA', 'MUPLU': 'PORT LOUIS', 'MVMLE': 'MALE', 'MXATM': 'ALTAMIRA', 'MXCOM': 'COSTA MAYA', 'MXCZM': 'COZUMEL', 'MXESE': 'ENSENADA', 'MXGYM': 'GUAYMAS', 'MXLZC': 'LAZARO CARDENAS', 'MXMZT': 'MAZATLAN', 'MXPGO': 'PROGRESO', 'MXPMS': 'PUERTO MORELOS', 'MXTAM': 'TAMPICO', 'MXTUY': 'TULUM', 'MXVER': 'VERACRUZ', 'MXZLO': 'MANZANILLO', 'MYBKI': 'KOTA KINABALU, SABAH', 'MYBTU': 'BINTULU, SARAWAK', 'MYKCH': 'KUCHING, SARAWAK', 'MYKUA': 'KUANTAN', 'MYLBU': 'LABUAN, SABAH', 'MYLGK': 'LANGKAWI', 'MYMKZ': 'MALACCA', 'MYMYY': 'MIRI, SARAWAK', 'MYPEN': 'PENANG', 'MYPGU': 'PASIR GUDANG, JOHOR', 'MYPKG': 'PORT KLANG (PELABUHAN KLANG)', 'MYSBW': 'SIBU, SARAWAK', 'MYSDK': 'SANDAKAN, SABAH', 'MYTPP': 'TANJUNG PELEPAS', 'MYTWU': 'TAWAU, SABAH', 'MZBEW': 'BEIRA', 'MZBZB': 'BAZARUTO ISLAND', 'MZMNC': 'NACALA', 'MZMPM': 'MAPUTO', 'MZMSG': 'MASSINGA', 'MZPOL': 'PEMBA', 'MZUEL': 'QUELIMANE', 'NALUD': 'LUDERITZ', 'NAWVB': 'WALVIS BAY', 'NCNOU': 'NOUMEA', 'NCVAV': 'VAVOUTO', 'NGAPP': 'APAPA', 'NGLKK': 'LEKKI', 'NGONN': 'ONNE', 'NGPHC': 'PORT HARCOURT', 'NGTIN': 'TINCAN/LAGOS', 'NICIO': 'CORINTO', 'NIMGA': 'MANAGUA', 'NLAMS': 'AMSTERDAM', 'NLFLU': 'FLUSHING', 'NLHRV': 'HEERENVEEN', 'NLIJM': 'IJMUIDEN', 'NLMOE': 'MOERDIJK', 'NLRTM': 'ROTTERDAM', 'NLVLI': 'VLISSINGEN', 'NOAES': 'ALESUND', 'NOALF': 'ALTA', 'NOALS': 'ALSTAHAUG', 'NOASV': 'AUSTEVOLL', 'NOBGO': 'BERGEN', 'NOBVK': 'BREVIK', 'NOEDF': 'EIDFJORD', 'NOEGE': 'EGERSUND', 'NOFLA': 'FLAM', 'NOFRK': 'FREDRIKSTAD', 'NOFRO': 'FLORO', 'NOGJM': 'GJEMNES', 'NOGNR': 'GEIRANGER', 'NOHAL': 'HALDEN', 'NOHAU': 'HAUGESUND', 'NOHOG': 'HOGSET', 'NOHVG': 'HONNINGSVAG', 'NOIKR': 'IKORNNES', 'NOKMY': 'KARMOY', 'NOKRS': 'KRISTIANSAND', 'NOKSU': 'KRISTIANSUND', 'NOKVD': 'KVINESDAL', 'NOLAR': 'LARVIK', 'NOLEK': 'LEIKANGER', 'NOLKN': 'LEKNES', 'NOLYR': 'LONGYEARBYEN', 'NOMAY': 'MALOY', 'NOMOL': 'MOLDE', 'NOMSS': 'MOSS', 'NONVK': 'NARVIK', 'NOOLD': 'OLDEN', 'NOORK': 'ORKANGER', 'NOOSL': 'OSLO', 'NOSAT': 'SALTEN', 'NOSAU': 'SAUDA', 'NOSUN': 'SUNNDALSORA', 'NOSVE': 'SVELGEN', 'NOSVG': 'STAVANGER', 'NOTAE': 'TANANGER', 'NOTOS': 'TROMSO', 'NOTRD': 'TRONDHEIM', 'NZAKL': 'AUCKLAND', 'NZBLU': 'BLUFF', 'NZCHC': 'CHRISTCHURCH', 'NZDUD': 'DUNEDIN', 'NZLYT': 'LYTTELTON', 'NZMAP': 'MARSDEN POINT', 'NZNPE': 'NAPIER', 'NZNSN': 'NELSON', 'NZPOE': 'PORT CHALMERS', 'NZTIU': 'TIMARU', 'NZTRG': 'TAURANGA', 'NZWLG': 'WELLINGTON', 'OMDQM': 'DUQM', 'OMKHS': 'KHASAB', 'OMMCT': 'MUSCAT', 'OMSLL': 'SALALAH', 'OMSOH': 'SOHAR', 'PABLB': 'BALBOA', 'PACTB': 'CRISTOBAL', 'PAMIT': 'MANZANILLO', 'PAONX': 'COLON', 'PAPAM': 'ALMIRANTE', 'PAPTY': 'PANAMA', 'PAROD': 'RODMAN', 'PECLL': 'CALLAO', 'PEPAI': 'PAITA', 'PEPIO': 'PISCO', 'PESVY': 'SALAVERRY', 'PFBOB': 'BORA-BORA', 'PFMOZ': 'MOOREA', 'PFPPT': 'PAPEETE', 'PGGUR': 'ALOTAU', 'PGLAE': 'LAE', 'PGLSA': 'LOSUIA', 'PGPOM': 'PORT MORESBY', 'PGRAB': 'RABAUL', 'PHBTG': 'BATANGAS, LUZON', 'PHCEB': 'CEBU', 'PHCGY': 'CAGAYAN DE ORO, MINDANAO', 'PHDVO': 'DAVAO, MINDANAO', 'PHGES': 'GENERAL SANTOS', 'PHMNN': 'MANILA NORTH HARBOUR', 'PHMNS': 'MANILA SOUTH HARBOUR', 'PHSFS': 'SUBIC', 'PKBQM': 'KARACHI-MUHAMMAD BIN QASIM', 'PKKHI': 'KARACHI', 'PLGDN': 'GDANSK', 'PLGDY': 'GDYNIA', 'PLSWI': 'SWINOUJSCIE', 'PLSZZ': 'SZCZECIN', 'PNPCN': 'PITCAIRN IS', 'PRSJU': 'SAN JUAN', 'PTAVE': 'AVEIRO', 'PTFDF': 'FIGUEIRA DA FOZ', 'PTFNC': 'FUNCHAL, MADEIRA', 'PTLEI': 'LEIXOES', 'PTLIS': 'LISBOA', 'PTPDL': 'PONTA DELGADA', 'PTPRM': 'PORTIMAO', 'PTSET': 'SETUBAL', 'PTSIE': 'SINES', 'PTSSB': 'SESIMBRA', 'PTTER': 'TERCEIRA ISLAND', 'PWROR': 'KOROR', 'PYBCM': 'CAACUPEMI ASUNCION', 'PYENO': 'ENCARNACION PUERTO SAN JUAN', 'PYPIL': 'CAACUPEMI PILAR', 'PYTVT': 'TERPORT VILLETA', 'PYVLL': 'PUERTO SEGURO FLUVIAL (VILLETA)', 'QADOH': 'DOHA', 'QAHMD': 'HAMAD', 'QAMES': 'MESAIEED', 'QARLF': 'RAS LAFFAN', 'REPDG': 'POINTE DES GALETS', 'REPOS': 'POSSESSION', 'ROAGI': 'AGIGEA', 'ROCND': 'CONSTANTA', 'ROGAL': 'GALATI', 'ROMAG': 'MANGALIA', 'RUARH': 'ARKHANGELSK', 'RUBLT': 'BALTIYSK', 'RUKDT': 'KRONSHTADT', 'RUKZP': 'KAVKAZ', 'RULED': 'SAINT PETERSBURG', 'RUNJK': 'NAKHODKA', 'RUNVS': 'NOVOROSSIYSK', 'RUPKC': 'PETROPAVLOVSK-KAMCHATSKIY', 'RUSKA': 'SLAVYANKA', 'RUSOC': 'SOCHI', 'RUULU': "UST'-LUGA", 'RUVVO': 'VLADIVOSTOK', 'RUVYP': 'VOSTOCHNIY, PORT', 'RUZAR': 'ZARUBINO', 'SADMM': 'AD DAMMAM', 'SAJED': 'JEDDAH', 'SAJUB': 'JUBAIL', 'SAKAC': 'KING ABDULLAH PORT', 'SANEO': 'NEOM', 'SAYNB': 'YANBU AL-BAHR', 'SBHIR': 'HONIARA, GUADALCANAL IS', 'SCPOV': 'PORT VICTORIA', 'SCVIC': 'VICTORIA', 'SDPZU': 'PORT SUDAN', 'SEAHU': 'AHUS', 'SEGOT': 'GOTEBORG', 'SEGVX': 'GAVLE', 'SEHAD': 'HALMSTAD', 'SEHEL': 'HELSINGBORG', 'SEKAN': 'KARLSHAMN', 'SENRK': 'NORRKOPING', 'SENYN': 'NYNASHAMN', 'SEPIT': 'PITEA', 'SESFT': 'SKELLEFTEA', 'SESKM': 'SKARHAMN', 'SESOE': 'SODERTALJE', 'SESTO': 'STOCKHOLM', 'SEVBY': 'VISBY', 'SGSIN': 'SINGAPORE', 'SHSHN': 'JAMESTOWN', 'SIKOP': 'KOPER', 'SLFNA': 'FREETOWN', 'SNDKR': 'DAKAR', 'SNZIG': 'ZIGUINCHOR', 'SOBBO': 'BERBERA', 'SOKMU': 'KISMAYU', 'SOMGQ': 'MOGADISHU', 'SRPBM': 'PARAMARIBO', 'SVAQJ': 'ACAJUTLA', 'SXPHI': 'PHILIPSBURG', 'SYLTK': 'LATTAKIA', 'SYTTS': 'TARTUS', 'TCGDT': 'GRAND TURK ISLAND', 'TCPLS': 'PROVIDENCIALES', 'TGLFW': 'LOME', 'THBKK': 'BANGKOK', 'THBMT': 'BANGKOK MODERN TERMINALS/BANGKOK', 'THHKT': 'PHUKET', 'THLCH': 'LAEM CHABANG', 'THLKR': 'LAT KRABANG', 'THPAT': 'PAT BANGKOK', 'THSBP': 'SIAM BANGKOK PORT', 'THSGZ': 'SONGKHLA', 'THTPT': 'THAI CONNECTIVITY TERMINAL', 'THUSM': 'KOH SAMUI', 'TLDIL': 'DILI', 'TNLGN': 'LA GOULETTE NORD (HALQUELOUED)', 'TNRDS': 'RADES/TUNIS', 'TNSFA': 'SFAX', 'TNSUS': 'SOUSSE', 'TNTUN': 'TUNIS', 'TOTBU': "NUKU'ALOFA", 'TRALA': 'ALANYA', 'TRALI': 'ALIAGA', 'TRAVC': 'AVCILAR', 'TRAYT': 'ANTALYA', 'TRBDM': 'BANDIRMA', 'TRBTS': 'BESIKTAS', 'TRBXN': 'BODRUM', 'TRBZC': 'BOZCAADA', 'TRCKZ': 'CANAKKALE', 'TRDRC': 'DERINCE', 'TREYP': 'EVYAP PORT', 'TRGEB': 'GEBZE', 'TRGEM': 'GEMLIK', 'TRGIR': 'GIRESUN', 'TRISK': 'ISKENDERUN', 'TRIST': 'ISTANBUL', 'TRITY': 'ISTINYE/BOSPHORUS', 'TRIZM': 'IZMIR', 'TRLMA': 'LIMAS', 'TRMER': 'MERSIN', 'TRMRM': 'MARMARIS', 'TRSSX': 'SAMSUN', 'TRTEK': 'TEKIRDAG (ASYAPORT)', 'TRTUZ': 'TUZLA', 'TRTZX': 'TRABZON', 'TRYAL': 'YALOVA', 'TRYAR': 'YARIMCA', 'TRZON': 'ZONGULDAK', 'TTPOS': 'PORT-OF-SPAIN', 'TTPTS': 'POINT LISAS', 'TTSCA': 'SCARBOROUGH/TOBAGO', 'TVFUN': 'FUNAFUTI', 'TWKEL': 'KEELUNG', 'TWKHH': 'KAOHSIUNG', 'TWTPE': 'TAIPEI', 'TWTXG': 'TAICHUNG', 'TZDAR': 'DAR ES SALAAM', 'TZMYW': 'MTWARA', 'TZTGT': 'TANGA', 'TZZNZ': 'ZANZIBAR', 'UAILK': 'CHORNOMORSK', 'UAIZM': 'IZMAIL', 'UAODS': 'ODESA', 'UARNI': 'RENI', 'UAYAL': 'YALTA', 'UAYUZ': 'YUZHNYY', 'USBAL': 'BALTIMORE', 'USBHB': 'BAR HARBOR', 'USBOS': 'BOSTON', 'USBRO': 'BROWNSVILLE', 'USCHS': 'CHARLESTON', 'USCLM': 'PT ANGELES', 'USCPV': 'CAPE CANAVERAL', 'USDUT': 'DUTCH HARBOR', 'USDVV': 'DAVISVILLE', 'USEVE': 'ELLISVILLE', 'USEWR': 'NEWARK', 'USEYW': 'KEY WEST', 'USFLL': 'FORT LAUDERDALE', 'USGPT': 'GULFPORT', 'USHNL': 'HONOLULU', 'USHOU': 'HOUSTON', 'USILG': 'WILMINGTON, DE', 'USILM': 'WILMINGTON, NC', 'USITO': 'HILO', 'USJAX': 'JACKSONVILLE', 'USKWH': 'KAWAIHAE', 'USLAX': 'LOS ANGELES', 'USLGB': 'LONG BEACH', 'USMIA': 'MIAMI', 'USMOB': 'MOBILE', 'USMSY': 'NEW ORLEANS', 'USNIJ': 'NAWILIWILI', 'USNPO': 'NEWPORT', 'USNTD': 'PORT HUENEME', 'USNYC': 'NEW YORK', 'USOAK': 'OAKLAND', 'USORF': 'NORFOLK', 'USPDX': 'PORTLAND, OR', 'USPEF': 'PORT EVERGLADES', 'USPHL': 'PHILADELPHIA', 'USPTM': 'PORTSMOUTH', 'USPWM': 'PORTLAND, ME', 'USSAV': 'SAVANNAH', 'USSEA': 'SEATTLE', 'USSFO': 'SAN FRANCISCO', 'USTIW': 'TACOMA', 'USTPA': 'TAMPA', 'USUAA': 'UNALASKA', 'UYMVD': 'MONTEVIDEO', 'UYNVP': 'NUEVA PALMIRA', 'UYPDP': 'PUNTA DEL ESTE', 'VCCRP': 'CAMPDEN PARK', 'VCKTN': 'KINGSTOWN, ST VINCENT', 'VEETV': 'EL TABLAZO/MARACAIBO L', 'VEGUB': 'GUARANAO BAY', 'VELAG': 'LA GUAIRA', 'VEPBL': 'PUERTO CABELLO', 'VEPCZ': 'PUERTO LA CRUZ', 'VGNSX': 'N. SOUND/VIRGIN GORDA', 'VGRAD': 'ROAD TOWN, TORTOLA', 'VICHA': 'CHARLOTTE AMALIE, ST THOMAS', 'VICTD': 'CHRISTIANSTED, SAINT CROIX', 'VISTT': 'SAINT THOMAS', 'VNDAD': 'DA-NANG', 'VNDNA': 'DONG NAI', 'VNHPH': 'HAIPHONG', 'VNNHA': 'NHA TRANG', 'VNPHG': 'PHUOC LONG', 'VNSGN': 'HO CHI MINH CITY', 'VNUIH': 'QUINHON', 'VNVUT': 'VUNG TAU', 'VUVLI': 'PORT VILA', 'WSAPW': 'APIA', 'YEADE': 'ADEN', 'YEHOD': 'HODEIDAH', 'YEMKX': 'MUKALLA', 'YTLON': 'LONGONI', 'ZACPT': 'CAPE TOWN', 'ZADUR': 'DURBAN', 'ZAELS': 'EAST LONDON', 'ZAMZY': 'MOSSEL BAY', 'ZAPLZ': 'PORT ELIZABETH', 'ZARCB': 'RICHARDS BAY', 'ZAZBA': 'COEGA'}
        self.current_file = None
        self.output_file = None

        # POL, TOL 선택 값 저장 변수
        self.selected_pol = tk.StringVar()
        self.selected_tol = tk.StringVar()

        # ITPS 관련 변수
        self.itps_file = None
        self.obl_file = None

        self.setup_ui()
        self.reset_all()  # 프로그램 시작 시 자동으로 초기화 실행

    def load_stowage_settings(self) -> Dict:
        """바탕화면의 Stowage 매핑 파일 로드"""
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            # 실제 매핑 파일 이름으로 수정 필요
            mapping_file = os.path.join(desktop, "stowage_mapping.json")
            with open(mapping_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Stowage 매핑 파일 로드 실패: {str(e)}")
            return {}

    def load_tpsz_settings(self) -> Dict:
        """바탕화면의 TpSz 매핑 파일 로드"""
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            # 실제 매핑 파일 이름으로 수정 필요
            mapping_file = os.path.join(desktop, "tpsz_mapping.json")
            with open(mapping_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"TpSz 매핑 파일 로드 실패: {str(e)}")
            return {}

    def setup_ui(self):
        # 탭 컨트롤 생성
        self.tab_control = ttk.Notebook(self.root)
        self.tab_control.pack(expand=True, fill="both")
        
        # 초기화 버튼 추가 (오른쪽 상단)
        reset_frame = ttk.Frame(self.root)
        reset_frame.pack(anchor='ne', padx=10, pady=5)
        
        reset_button = ttk.Button(reset_frame, text="초기화", command=self.reset_all)
        reset_button.pack()
        
        # 기존 단일 CLL 변환 탭
        self.single_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.single_tab, text='단일 CLL 변환')
        
        # Multi CLL 변환 탭
        self.multi_cll_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.multi_cll_tab, text='Multi CLL 변환')
        
        # ITPS 추가 탭
        self.itps_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.itps_tab, text='ITPS 추가')

        # STOWAGE CODE 관리 탭
        self.stowage_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.stowage_tab, text='STOWAGE CODE 관리')

        # TpSZ 관리 탭
        self.tpsz_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tpsz_tab, text='TpSZ 관리')

        # 각 탭 설정
        self.setup_single_tab()  # 단일 CLL 탭 설정
        self.setup_multi_cll_tab()  # Multi CLL 탭 설정
        self.setup_itps_tab()  # ITPS 탭 설정
        self.setup_stowage_tab()  # STOWAGE CODE 탭 설정
        self.setup_tpsz_tab()  # TpSZ 탭 설정

    def setup_single_tab(self):
        # 단일 CLL 변환 탭 설정
        left_frame = ttk.Frame(self.single_tab)
        left_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        right_frame = ttk.Frame(self.single_tab)
        right_frame.pack(side="right", fill="both", padx=5)
        
        # POL, TOL 선택 프레임
        port_frame = ttk.LabelFrame(left_frame, text="항구 선택")
        port_frame.pack(pady=10, padx=10, fill="x")

        # POL 버튼 프레임
        pol_frame = ttk.LabelFrame(port_frame, text="POL")
        pol_frame.pack(pady=5, padx=5, fill="x")

        # POL 버튼들
        pol_ports = ['KRPUS', 'KRKAN', 'KRINC']
        self.pol_buttons = {}
        for port in pol_ports:
            btn = tk.Button(pol_frame, text=port, width=10,
                          command=lambda p=port: self.select_pol(p))
        btn.pack(side=tk.LEFT, padx=5, pady=5)
        self.pol_buttons[port] = btn

        # TOL 버튼 프레임
        tol_frame = ttk.LabelFrame(port_frame, text="TOL")
        tol_frame.pack(pady=5, padx=5, fill="x")

        # TOL 버튼들과 매핑
        tol_mapping = {
            'PNC': 'KRPUSPN',
            'PNIT': 'KRPUSAB',
            'BCT': 'KRPUSBC',
            'HJNC': 'KRPUSAP',
            'ICT': 'KRINCAH',
            'GWCT': 'KRKANKT'
        }
        self.tol_buttons = {}
        self.tol_values = tol_mapping
        for btn_text, value in tol_mapping.items():
            btn = tk.Button(tol_frame, text=btn_text, width=10,
                          command=lambda v=value: self.select_tol(v))
            btn.pack(side=tk.LEFT, padx=5, pady=5)
            self.tol_buttons[value] = btn

        # 파일 정보 표시 영역
        info_frame = ttk.LabelFrame(left_frame, text="파일 정보")
        info_frame.pack(pady=10, padx=10, fill="x")

        self.input_label = ttk.Label(info_frame, text="입력 파일: 없음")
        self.input_label.pack(pady=5, anchor="w")

        self.output_label = ttk.Label(info_frame, text="출력 파일: 없음")
        self.output_label.pack(pady=5, anchor="w")

        # CLL 변환을 위한 드래그 & 드롭 영역
        self.cll_frame = ttk.LabelFrame(left_frame, text="CLL -> OBL 변환")
        self.cll_frame.pack(pady=10, padx=10, fill="x")

        self.cll_label = ttk.Label(self.cll_frame, text="CLL 파일을 여기에 드롭하세요")
        self.cll_label.pack(pady=20)

        # CLL 드래그 앤 드롭 바인딩
        self.cll_label.drop_target_register(DND_FILES)
        self.cll_label.dnd_bind('<<Drop>>', self.drop_cll_file)

        # OBL EMPTY 추가를 위한 드래그 & 드롭 영역
        self.obl_frame = ttk.LabelFrame(left_frame, text="OBL EMPTY 추가")
        self.obl_frame.pack(pady=10, padx=10, fill="x")

        self.obl_label = ttk.Label(self.obl_frame, text="OBL 파일을 여기에 드롭하세요")
        self.obl_label.pack(pady=20)

        # OBL 드래그 앤 드롭 바인딩
        self.obl_label.drop_target_register(DND_FILES)
        self.obl_label.dnd_bind('<<Drop>>', self.drop_obl_file)

        # EMPTY 컨테이너 입력 섹션
        empty_frame = ttk.LabelFrame(left_frame, text="EMPTY 컨테이너 추가")
        empty_frame.pack(pady=10, padx=10, fill="x")

        # 5개의 입력 행 생성
        self.empty_entries = []
        for i in range(5):
            row_frame = ttk.Frame(empty_frame)
            row_frame.pack(pady=5)

            pod_entry = ttk.Entry(row_frame, width=10)
            pod_entry.pack(side="left", padx=5)
            pod_entry.insert(0, "POD")
            pod_entry.bind('<FocusIn>', lambda e, entry=pod_entry: self.on_entry_click(e, entry))
            pod_entry.bind('<FocusOut>', lambda e, entry=pod_entry: self.on_focus_out(e, entry, "POD"))
            pod_entry.bind('<Key>', lambda e, entry=pod_entry: self.on_key_press(e, entry))

            sztp_entry = ttk.Entry(row_frame, width=10)
            sztp_entry.pack(side="left", padx=5)
            sztp_entry.insert(0, "SzTp")
            sztp_entry.bind('<FocusIn>', lambda e, entry=sztp_entry: self.on_entry_click(e, entry))
            sztp_entry.bind('<FocusOut>', lambda e, entry=sztp_entry: self.on_focus_out(e, entry, "SzTp"))
            sztp_entry.bind('<Key>', lambda e, entry=sztp_entry: self.on_key_press(e, entry))

            qty_entry = ttk.Entry(row_frame, width=5)
            qty_entry.pack(side="left", padx=5)
            qty_entry.insert(0, "수량")
            qty_entry.bind('<FocusIn>', lambda e, entry=qty_entry: self.on_entry_click(e, entry))
            qty_entry.bind('<FocusOut>', lambda e, entry=qty_entry: self.on_focus_out(e, entry, "수량"))
            qty_entry.bind('<Key>', lambda e, entry=qty_entry: self.on_key_press(e, entry))

            self.empty_entries.append((pod_entry, sztp_entry, qty_entry))

        # Summary 표시 영역을 right_frame으로 이동
        self.single_summary_frame = ttk.LabelFrame(right_frame, text="Container Summary")
        self.single_summary_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.single_summary_text = tk.Text(self.single_summary_frame, height=30, width=40)
        self.single_summary_text.pack(pady=5, padx=5, fill="both", expand=True)
        self.single_summary_text.insert(tk.END, "단일 CLL 탭에서 파일 변환 시 Summary가 표시됩니다.")

    def setup_multi_cll_tab(self):
        """CLL 파일 병합 탭 설정"""
        # 좌우 분할
        left_frame = ttk.Frame(self.multi_cll_tab)
        left_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        right_frame = ttk.Frame(self.multi_cll_tab)
        right_frame.pack(side="right", fill="both", padx=5)
        
        # POL/TOL 선택 프레임
        port_frame = ttk.LabelFrame(left_frame, text="항구 선택")
        port_frame.pack(pady=10, padx=10, fill="x")
        
        # POL 버튼 프레임
        pol_frame = ttk.LabelFrame(port_frame, text="POL")
        pol_frame.pack(pady=5, padx=5, fill="x")
        
        pol_ports = ['KRPUS', 'KRKAN', 'KRINC']
        self.multi_pol_buttons = {}
        for port in pol_ports:
            btn = tk.Button(pol_frame, text=port, width=10,
                          command=lambda p=port: self.select_multi_pol(p))
            btn.pack(side=tk.LEFT, padx=5, pady=5)
            self.multi_pol_buttons[port] = btn

        # TOL 버튼 프레임
        tol_frame = ttk.LabelFrame(port_frame, text="TOL")
        tol_frame.pack(pady=5, padx=5, fill="x")
        
        tol_mapping = {
            'PNC': 'KRPUSPN',
            'PNIT': 'KRPUSAB',
            'BCT': 'KRPUSBC',
            'HJNC': 'KRPUSAP',
            'ICT': 'KRINCAH',
            'GWCT': 'KRKANKT'
        }
        
        self.multi_tol_buttons = {}
        for btn_text, value in tol_mapping.items():
            btn = tk.Button(tol_frame, text=btn_text, width=10,
                          command=lambda v=value: self.select_multi_tol(v))
            btn.pack(side=tk.LEFT, padx=5, pady=5)
            self.multi_tol_buttons[btn_text] = btn

        # 파일 선택 영역 컨테이너
        files_frame = ttk.Frame(left_frame)
        files_frame.pack(pady=10, padx=10, fill="x")

        # Master CLL 파일 프레임
        self.master_frame = ttk.LabelFrame(files_frame, text="첫 번째(Master) CLL 파일")
        self.master_frame.pack(pady=5, padx=5, fill="x")
        
        self.master_label = ttk.Label(self.master_frame, text="CLL 파일을 여기에 드롭하세요")
        self.master_label.pack(pady=10)
        
        self.master_path_label = ttk.Label(self.master_frame, text="파일 경로: 없음")
        self.master_path_label.pack(pady=5)
        
        # Master 파일 드롭 영역 바인딩
        self.master_frame.drop_target_register(DND_FILES)
        self.master_frame.dnd_bind('<<Drop>>', self.drop_master_cll)

        # Slave CLL 파일 프레임
        self.slave_frame = ttk.LabelFrame(files_frame, text="두 번째(Slave) CLL 파일")
        self.slave_frame.pack(pady=5, padx=5, fill="x")
        
        self.slave_label = ttk.Label(self.slave_frame, text="CLL 파일을 여기에 드롭하세요")
        self.slave_label.pack(pady=10)
        
        self.slave_path_label = ttk.Label(self.slave_frame, text="파일 경로: 없음")
        self.slave_path_label.pack(pady=5)
        
        # Slave 파일 드롭 영역 바인딩
        self.slave_frame.drop_target_register(DND_FILES)
        self.slave_frame.dnd_bind('<<Drop>>', self.drop_slave_cll)

        # 결과 정보 프레임
        self.result_frame = ttk.LabelFrame(right_frame, text="변환 결과")
        self.result_frame.pack(pady=10, padx=10, fill="x")
        
        self.result_label = ttk.Label(self.result_frame, text="출력 파일: 없음")
        self.result_label.pack(pady=5)

        # Summary 표시 영역을 right_frame으로 이동
        self.multi_summary_frame = ttk.LabelFrame(right_frame, text="Container Summary")
        self.multi_summary_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.multi_summary_text = tk.Text(self.multi_summary_frame, height=30, width=40)
        self.multi_summary_text.pack(pady=5, padx=5, fill="both", expand=True)
        self.multi_summary_text.insert(tk.END, "Multi CLL 탭에서 파일 변환 시 Summary가 표시됩니다.")

    def setup_itps_tab(self):
        """ITPS 추가 탭 설정"""
        # 좌우 분할
        left_frame = ttk.Frame(self.itps_tab)
        left_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        right_frame = ttk.Frame(self.itps_tab)
        right_frame.pack(side="right", fill="both", padx=5)

        # 파일 정보 표시 영역
        info_frame = ttk.LabelFrame(left_frame, text="파일 정보")
        info_frame.pack(pady=10, padx=10, fill="x")

        self.itps_input_label = ttk.Label(info_frame, text="ITPS 파일: 없음")
        self.itps_input_label.pack(pady=5, anchor="w")

        self.itps_obl_label = ttk.Label(info_frame, text="OBL 파일: 없음")
        self.itps_obl_label.pack(pady=5, anchor="w")

        self.itps_output_label = ttk.Label(info_frame, text="출력 파일: 없음")
        self.itps_output_label.pack(pady=5, anchor="w")

        # ITPS 파일 드롭 영역
        itps_drop_frame = ttk.LabelFrame(left_frame, text="ITPS 파일 드롭")
        itps_drop_frame.pack(pady=10, padx=10, fill="x")

        self.itps_drop_label = ttk.Label(itps_drop_frame, text="ITPS 파일을 여기에 드롭하세요")
        self.itps_drop_label.pack(pady=20)

        # ITPS 드래그 앤 드롭 바인딩
        self.itps_drop_label.drop_target_register(DND_FILES)
        self.itps_drop_label.dnd_bind('<<Drop>>', self.drop_itps_file)

        # OBL 파일 드롭 영역
        obl_drop_frame = ttk.LabelFrame(left_frame, text="OBL 파일 드롭")
        obl_drop_frame.pack(pady=10, padx=10, fill="x")

        self.obl_drop_label = ttk.Label(obl_drop_frame, text="OBL 파일을 여기에 드롭하세요")
        self.obl_drop_label.pack(pady=20)

        # OBL 드래그 앤 드롭 바인딩
        self.obl_drop_label.drop_target_register(DND_FILES)
        self.obl_drop_label.dnd_bind('<<Drop>>', self.drop_obl_for_itps)

        # Summary 표시 영역
        self.itps_summary_frame = ttk.LabelFrame(right_frame, text="ITPS Summary")
        self.itps_summary_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.itps_summary_text = tk.Text(self.itps_summary_frame, height=30, width=40)
        self.itps_summary_text.pack(pady=5, padx=5, fill="both", expand=True)
        self.itps_summary_text.insert(tk.END, "ITPS 파일 처리 시 Summary가 표시됩니다.")

    def setup_stowage_tab(self):
        """STOWAGE CODE 관리 탭 설정"""
        # 메인 프레임
        main_frame = ttk.Frame(self.stowage_tab)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 서비스 선택 프레임
        service_frame = ttk.LabelFrame(main_frame, text="Service Name 선택")
        service_frame.pack(fill="x", pady=(0, 10))
        
        # 서비스 선택 콤보박스
        self.selected_service = tk.StringVar()
        self.service_combo = ttk.Combobox(service_frame, textvariable=self.selected_service)
        self.service_combo.pack(pady=10, padx=5, fill="x")
        self.service_combo.bind('<<ComboboxSelected>>', self.on_service_selected)

        # 드래그 & 드롭 영역
        drop_frame = ttk.LabelFrame(main_frame, text="Stowage Code 엑셀 파일")
        drop_frame.pack(fill="x", pady=(0, 10))

        self.stowage_drop_label = ttk.Label(drop_frame, text="Stowage Code 엑셀 파일을 여기에 드롭하세요")
        self.stowage_drop_label.pack(pady=20)

        # 드래그 앤 드롭 바인딩
        self.stowage_drop_label.drop_target_register(DND_FILES)
        self.stowage_drop_label.dnd_bind('<<Drop>>', self.drop_stowage_file)

        # 컬럼 매핑 설정 영역
        mapping_frame = ttk.LabelFrame(main_frame, text="컬럼 매핑 설정")
        mapping_frame.pack(fill="x", pady=(0, 10))

        # Discharge Port 컬럼 매핑
        discharge_frame = ttk.Frame(mapping_frame)
        discharge_frame.pack(fill="x", pady=5)
        ttk.Label(discharge_frame, text="Discharge Port 컬럼명:").pack(side="left", padx=5)
        self.discharge_entry = ttk.Entry(discharge_frame)
        self.discharge_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.discharge_entry.insert(0, self.stow_column_mapping.get('discharge_port', ''))

        # Stowage Code 컬럼 매핑
        stowage_frame = ttk.Frame(mapping_frame)
        stowage_frame.pack(fill="x", pady=5)
        ttk.Label(stowage_frame, text="Stowage Code 컬럼명:").pack(side="left", padx=5)
        self.stowage_entry = ttk.Entry(stowage_frame)
        self.stowage_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.stowage_entry.insert(0, self.stow_column_mapping.get('stowage_code', ''))

        # 저장 버튼
        save_button = ttk.Button(mapping_frame, text="설정 저장", command=self.save_stowage_settings)
        save_button.pack(pady=10)

        # 현재 매핑 미리보기
        preview_frame = ttk.LabelFrame(main_frame, text="현재 매핑 미리보기")
        preview_frame.pack(fill="both", expand=True)
        
        self.preview_text = tk.Text(preview_frame, height=10)
        self.preview_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 현재 매핑 표시
        self.update_stowage_preview()

    def on_service_selected(self, event):
        """서비스 선택 시 처리"""
        self.update_stowage_preview()

    def on_entry_click(self, event, entry):
        """Entry 위젯 클릭시 기본 텍스트 제거"""
        if entry.get() in ["POD", "SzTp", "수량"]:
            entry.delete(0, tk.END)
            entry.config(foreground='black')

    def on_focus_out(self, event, entry, default_text):
        """Entry 위젯에서 포커스가 빠졌을 때 처리"""
        if entry.get().strip() == "":
            entry.insert(0, default_text)
            entry.config(foreground='gray')

    def on_key_press(self, event, entry):
        """키 입력 처리"""
        if entry.get() in ["POD", "SzTp", "수량"]:
            entry.delete(0, tk.END)

    def on_tab(self, event):
        """탭 키 처리"""
        current = event.widget
        next_widget = current.tk_focusNext()
        next_widget.focus()
        return "break"  # 기본 탭 동작 방지

    def drop_cll_file(self, event):
        """단일 CLL 파일 드롭 처리"""
        if not self.selected_pol.get() or not self.selected_tol.get():
            messagebox.showwarning("경고", "POL과 TOL을 먼저 선택해주세요!")
            return

        file_path = event.data.strip('{}').strip('"')
        if not os.path.exists(file_path):
            messagebox.showerror("오류", "파일이 존재하지 않습니다.")
            return

        try:
            # CLL 파일 읽기
            df = pd.read_excel(file_path, header=4)
            
            # 데이터 변환 및 저장
            self.current_file = file_path
            self.input_label.config(text=f"입력 파일: {os.path.basename(file_path)}")
            
            # 단일 탭의 Summary만 업데이트
            self.update_single_summary(df)
            
            # 멀티 탭의 Summary는 초기화
            if hasattr(self, 'multi_summary_text'):
                self.multi_summary_text.delete(1.0, tk.END)
                self.multi_summary_text.insert(tk.END, "Multi CLL 탭에서 파일 병합 시 Summary가 표시됩니다.")
            
            self.convert_file()
            
        except Exception as e:
            print(f"Error in drop_cll_file: {str(e)}")  # 디버깅용
            messagebox.showerror("오류", f"파일 처리 중 오류가 발생했습니다: {str(e)}")

    def drop_obl_file(self, event):
        """OBL 파일 드롭 처리"""
        file_path = event.data
        file_path = file_path.strip('{}')
        self.current_file = file_path

        # 파일 정보 표시 업데이트
        self.input_label.config(text=f"입력 파일: {file_path}")
        self.obl_label.config(text=f"선택된 파일: {os.path.basename(file_path)}")

        # EMPTY 컨테이너 추가 실행
        self.add_empty_to_obl()

    def add_empty_to_obl(self):
        """기존 OBL에 EMPTY 컨테이너 추가"""
        # OBL 파일 읽기
        obl_df = pd.read_excel(self.current_file)

        # 기존 OBL의 컬럼 목록 가져오기
        existing_columns = obl_df.columns.tolist()

        # EMPTY 컨테이너 추가
        new_rows = []
        empty_container_num = 1  # 컨테이너 번호 시작값
        
        for pod_entry, sztp_entry, qty_entry in self.empty_entries:
            pod = pod_entry.get()
            sztp = sztp_entry.get()
            qty = qty_entry.get()

            if pod not in ["POD", ""] and sztp not in ["SzTp", ""] and qty not in ["수량", ""]:
                try:
                    qty = int(qty)
                    # SzTp를 정수로 변환
                    sztp = int(sztp)
                    
                    # SzTp에 따른 무게 설정
                    if str(sztp).startswith('2'):
                        weight = 2500
                    elif str(sztp).startswith('4'):
                        weight = 4500
                    else:
                        weight = 0

                    for i in range(qty):
                        # 기존 컬럼 구조를 따르는 빈 딕셔너리 생성
                        empty_row = {col: '' for col in existing_columns}

                        # 마지막 No 값 계산
                        last_no = len(obl_df) + len(new_rows) + 1

                        # EMPTY 컨테이너 번호 생성
                        ctr_nbr = f"MSCU{empty_container_num:07d}"
                        empty_container_num += 1

                        # 필요한 필드만 업데이트
                        empty_row.update({
                            'No': last_no,
                            'CtrNbr': ctr_nbr,  # 컨테이너 번호 설정
                            'ShOwn': 'N',
                            'Opr': 'MSC',
                            'POR': self.selected_pol.get(),
                            'POL': self.selected_pol.get(),
                            'TOL': self.selected_tol.get(),
                            'POD': pod,
                            'FPOD': pod,  # POD와 동일한 값으로 설정
                            'SzTp': sztp,
                            'Wgt': weight,  # SzTp에 따른 무게 설정
                            'ForE': 'E',
                            'Rfopr': 'N',
                            'Door': 'C',
                            'CustH': 'N',
                            'Fumi': 'N',
                            'VGM': 'Y',
                            'Stow': self.stow_mapping.get(pod, '')  # FPOD(POD)에 대한 Stow 코드
                        })
                        new_rows.append(empty_row)
                except ValueError:
                    continue  # 잘못된 입력은 조용히 건너뛰기

        # 새로운 EMPTY 컨테이너 추가
        if new_rows:
            new_df = pd.DataFrame(new_rows, columns=existing_columns)
            obl_df = pd.concat([obl_df, new_df], ignore_index=True)

            # 파일 저장
            input_dir = os.path.dirname(self.current_file)
            base_name = os.path.splitext(os.path.basename(self.current_file))[0]
            output_file = os.path.join(input_dir, f"{base_name}_EMPTY_ADDED.xlsx")
            obl_df.to_excel(output_file, index=False)

            self.output_file = output_file
            self.output_label.config(text=f"출력 파일: {output_file}")

            # Summary 업데이트
            self.update_summary(obl_df)

            messagebox.showinfo("성공", "EMPTY 컨테이너가 추가되었습니다.")

    def update_summary(self, df):
        """컨테이너 요약 정보 업데이트"""
        summary = "=== FULL 컨테이너 ===\n"
        full_containers = df[df['F/E'] == 'F']
        full_summary = full_containers['T&S'].value_counts()
        for sztp, count in full_summary.items():
            summary += f"{sztp}: {count}개\n"
        summary += f"FULL 컨테이너 총계: {len(full_containers)}개\n"

        summary += "\n=== EMPTY 컨테이너 ===\n"
        empty_containers = df[df['F/E'] == 'E']
        empty_summary = empty_containers['T&S'].value_counts()
        for sztp, count in empty_summary.items():
            summary += f"{sztp}: {count}개\n"

        # EMPTY 입력란에서 추가될 컨테이너 계산
        additional_empty = 0
        for pod_entry, sztp_entry, qty_entry in self.empty_entries:
            qty = qty_entry.get()
            if qty not in ["수량", ""]:
                try:
                    additional_empty += int(qty)
                except ValueError:
                    pass

        total_empty = len(empty_containers) + additional_empty
        summary += f"EMPTY 컨테이너 총계: {total_empty}개\n"

        # 전체 총계
        summary += f"\n=== 전체 컨테이너 ===\n"
        summary += f"총계: {len(full_containers) + total_empty}개"

        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, summary)

    def select_pol(self, port):
        """POL 버튼 선택 처리"""
        self.selected_pol.set(port)
        # 모든 버튼 원래 색으로
        for btn in self.pol_buttons.values():
            btn.configure(bg='SystemButtonFace')
        # 선택된 버튼만 노란색으로
        self.pol_buttons[port].configure(bg='yellow')

    def select_tol(self, terminal):
        """TOL 버튼 선택 처리"""
        self.selected_tol.set(terminal)
        # 모든 버튼 원래 색으로
        for btn in self.tol_buttons.values():
            btn.configure(bg='SystemButtonFace')
        # 선택된 버튼만 노란색으로
        self.tol_buttons[terminal].configure(bg='yellow')

    def convert_file(self):
        """단일 CLL 파일 변환"""
        try:
            # 선택된 서비스 확인
            selected_service = self.selected_service.get()
            if not selected_service:
                messagebox.showwarning("경고", "Service Name을 선택해주세요!")
                return

            # CLL 파일 읽기
            cll_df = pd.read_excel(self.current_file, header=4)

            # 선택된 서비스의 매핑 가져오기
            service_mappings = self.stow_mapping.get(selected_service, [])

            # OBL 데이터프레임 생성
            obl_data = []

            # CLL 데이터 변환
            for idx, row in cll_df.iterrows():
                # OPT가 비어있으면 선택된 POL 값 사용
                por_value = row['OPT'] if pd.notna(row['OPT']) and row['OPT'] != '' else self.selected_pol.get()

                # POD와 FPOD 처리
                pod = str(row['POD']) if pd.notna(row['POD']) else ''
                fpod = str(row['FDP']) if pd.notna(row['FDP']) else ''  # FPOD는 CLL의 FDP 값 사용
                
                # 초기값 설정
                mapped_port = pod  # POD 초기값
                mapped_stow = ''   # Stow 초기값
                
                # POD가 stow_code와 일치하는지 확인
                for mapping in service_mappings:
                    if pod.upper() == mapping['stow_code'].upper():
                        mapped_port = mapping['port']      # POD를 port 값으로 설정
                        mapped_stow = mapping['stow_code'] # Stow를 stow_code 값으로 설정
                        break

                obl_row = {
                    'No': idx + 1,
                    'CtrNbr': row['CNTR NO'],
                    'ShOwn': 'N',
                    'Opr': 'MSC',
                    'POR': por_value,
                    'POL': self.selected_pol.get(),
                    'TOL': self.selected_tol.get(),
                    'POD': mapped_port,
                    'TOD': '',
                    'Stow': mapped_stow,
                    'FPOD': fpod,  # FPOD는 원래 값 유지
                    'SzTp': int(row['T&S']) if pd.notna(row['T&S']) else '',
                    'Wgt': int(row['WGT']) if pd.notna(row['WGT']) else '',
                    'ForE': row['F/E'],
                    'Lbl': '',
                    'Rfopr': 'N',
                    'Rftemp': row['R/F'].replace(' CEL', '') if pd.notna(row['R/F']) else '',
                    'OvDH': row['OH'],
                    'OvDF': row['OL'] / 2 if pd.notna(row['OL']) and row['OL'] != 0 else '',
                    'OvDA': row['OL'] / 2 if pd.notna(row['OL']) and row['OL'] != 0 else '',
                    'OvDP': row['OW'] / 2 if pd.notna(row['OW']) and row['OW'] != 0 else '',
                    'OvDS': row['OW'] / 2 if pd.notna(row['OW']) and row['OW'] != 0 else '',
                    'OvSH': '',
                    'OvSF': '',
                    'OvSA': '',
                    'OvSP': '',
                    'OvSS': '',
                    'BL': '',
                    'HI': '',
                    'AC': '',
                    'Flip': '',
                    'Door': 'C',
                    'CustH': 'N',
                    'LenBB': '',
                    'BrthBB': '',
                    'HgtBB': '',
                    'WgtBB': '',
                    'Fumi': 'N',
                    'FuDt': '',
                    'VenDt': '',
                    'Venti': '',
                    'Damag': '',
                    'PPK': '',
                    'Food': '',
                    'Resi': '',
                    'Book': '',
                    'Cold': '',
                    'Catm': '',
                    'VGM': 'Y',
                    'VGM Weighting Method': '',
                    'HVC': '',
                    'BN1': '',
                    'BN2': '',
                    'BN3': '',
                    'BN4': '',
                    'Harmonised system codes': '',
                    'Description': '',
                    'Flexitank': '',
                    'UNNO': row['UNDG'],
                    'Class': row['IMDG'],
                    'PSN': '',
                    'N.Weight': '',
                    'S.Risk1': '',
                    'S.Risk2': '',
                    'S.Risk3': '',
                    'P.Group': '',
                    'LQ': '',
                    'EQ': '',
                    'FP': '',
                    'IMDG Remark': '',
                    'Sub Index': '',
                    'Inf type': '',
                    'Address': '',
                    'Street': '',
                    'City': '',
                    'Postal Code': '',
                    'Country Code': '',
                    'Country': '',
                    'Remark': ''
                }
                obl_data.append(obl_row)

            # EMPTY 컨테이너 추가 로직
            last_no = len(obl_data)
            empty_container_num = 1
            for pod_entry, sztp_entry, qty_entry in self.empty_entries:
                pod = pod_entry.get()
                sztp = sztp_entry.get()
                qty = qty_entry.get()

                if pod not in ["POD", ""] and sztp not in ["SzTp", ""] and qty not in ["수량", ""]:
                    try:
                        qty = int(qty)
                        for i in range(qty):
                            empty_row = dict.fromkeys(obl_data[0].keys(), '')
                            
                            # POD에 대한 매핑 확인
                            mapped_port = pod
                            mapped_stow = ''
                            
                            # POD가 stow_code와 일치하는지 확인
                            for mapping in service_mappings:
                                if pod.upper() == mapping['stow_code'].upper():
                                    # stow_code가 일치하면 해당 port를 POD로 사용
                                    mapped_port = mapping['port']
                                    mapped_stow = mapping['stow_code']
                                    break
                                elif pod.upper() == mapping['port'].upper():
                                    # port가 일치하면 해당 stow_code 사용
                                    mapped_port = mapping['port']
                                    mapped_stow = mapping['stow_code']
                                    break
                            
                            empty_row.update({
                                'No': last_no + 1,
                                'CtrNbr': f"MSCU{empty_container_num:07d}",
                                'ShOwn': 'N',
                                'Opr': 'MSC',
                                'POR': self.selected_pol.get(),
                                'POL': self.selected_pol.get(),
                                'TOL': self.selected_tol.get(),
                                'POD': mapped_port,
                                'FPOD': mapped_port,
                                'SzTp': int(sztp),
                                'Wgt': int(2500 if str(sztp).startswith('2') else 4700 if str(sztp).startswith('4') else 0),
                                'ForE': 'E',
                                'Rfopr': 'N',
                                'Door': 'C',
                                'CustH': 'N',
                                'Fumi': 'N',
                                'VGM': 'Y',
                                'Stow': mapped_stow
                            })
                            obl_data.append(empty_row)
                            last_no += 1
                            empty_container_num += 1
                    except ValueError:
                        messagebox.showwarning("경고", f"잘못된 수량 형식: {qty}")

            # OBL 데이터프레임 생성
            obl_df = pd.DataFrame(obl_data)

            # 파일 저장
            input_dir = os.path.dirname(self.current_file)
            base_name = os.path.splitext(os.path.basename(self.current_file))[0]
            output_file = os.path.join(input_dir, f"{base_name}_OBL.xlsx")
            obl_df.to_excel(output_file, index=False)

            self.output_file = output_file
            self.output_label.config(text=f"출력 파일: {output_file}")

            # 단일 탭의 Summary만 업데이트
            self.update_single_summary(cll_df)
            
            messagebox.showinfo("성공", "변환이 완료되었습니다.")

        except Exception as e:
            messagebox.showerror("Error", f"변환 중 오류 발생: {str(e)}")

    def update_single_summary(self, df):
        """단일 CLL 파일의 Container Summary 업데이트"""
        try:
            self.single_summary_text.delete(1.0, tk.END)
            
            summary_text = "=== 단일 CLL 변환 Summary ===\n"
            summary_text += "================================\n\n"
            
            # 데이터프레임 유효성 검사
            if df is None or df.empty:
                raise ValueError("유효한 데이터가 없습니다.")
            
            # 컬럼 존재 여부 확인
            required_columns = ['T&S', 'F/E', 'POD']
            for col in required_columns:
                if col not in df.columns:
                    raise ValueError(f"필요한 컬럼이 없습니다: {col}")
            
            # 데이터 처리
            total_containers = len(df)
            
            # 각 컬럼별 카운트 계산 (NaN 값 제외)
            size_type_counts = df['T&S'].dropna().value_counts()
            full_empty_counts = df['F/E'].dropna().value_counts()
            pod_counts = df['POD'].dropna().value_counts()
            
            # Summary 텍스트 구성
            summary_text += f"Total Containers: {total_containers}\n"
            summary_text += "--------------------------------\n\n"
            
            summary_text += "=== Size Type Summary ===\n"
            for sz_tp, count in size_type_counts.items():
                if pd.notna(sz_tp):  # NaN 값 체크
                    summary_text += f"{sz_tp}: {count}\n"
            summary_text += "--------------------------------\n\n"
            
            summary_text += "=== Full/Empty Summary ===\n"
            for fe, count in full_empty_counts.items():
                if pd.notna(fe):  # NaN 값 체크
                    summary_text += f"{fe}: {count}\n"
            summary_text += "--------------------------------\n\n"
            
            summary_text += "=== POD Summary ===\n"
            for pod, count in pod_counts.items():
                if pd.notna(pod):  # NaN 값 체크
                    summary_text += f"{pod}: {count}\n"
            summary_text += "--------------------------------"
            
            self.single_summary_text.insert(tk.END, summary_text)
            
        except Exception as e:
            print(f"Summary 생성 중 오류 발생: {str(e)}")  # 디버깅용
            self.single_summary_text.delete(1.0, tk.END)
            self.single_summary_text.insert(tk.END, "단일 CLL 탭에서 파일 변환 시 Summary가 표시됩니다.")

    def drop_master_cll(self, event):
        """Master CLL 파일 드롭 처리"""
        if not self.selected_pol.get() or not self.selected_tol.get():
            messagebox.showwarning("경고", "POL과 TOL을 먼저 선택해주세요!")
            return

        file_path = event.data.strip('{}').strip('"')
        if not os.path.exists(file_path):
            messagebox.showerror("오류", "파일이 존재하지 않습니다.")
            return

        self.master_file = file_path
        self.master_path_label.config(text=f"파일 경로: {file_path}")
        self.master_label.config(text="Master 파일이 선택되었습니다")
        
        # Slave 프레임 활성화
        self.slave_frame.pack(pady=10, padx=10, fill="x")

    def drop_slave_cll(self, event):
        """Slave CLL 파일 드롭 처리"""
        if not hasattr(self, 'master_file'):
            messagebox.showwarning("경고", "Master 파일을 먼저 선택해주세요!")
            return

        file_path = event.data.strip('{}').strip('"')
        if not os.path.exists(file_path):
            messagebox.showerror("오류", "파일이 존재하지 않습니다.")
            return

        self.slave_file = file_path
        self.slave_path_label.config(text=f"파일 경로: {file_path}")
        self.slave_label.config(text="Slave 파일이 선택되었습니다")
        
        # Slave 파일이 선택되면 바로 병합 처리 시작
        self.combine_cll_files()

    def select_multi_pol(self, port):
        """Multi 탭 POL 버튼 선택 처리"""
        self.selected_pol.set(port)
        # 모든 버튼 원래 색으로
        for btn in self.multi_pol_buttons.values():
            btn.configure(bg='SystemButtonFace')
        # 선택된 버튼만 노란색으로
        self.multi_pol_buttons[port].configure(bg='yellow')

    def select_multi_tol(self, terminal):
        """Multi 탭 TOL 버튼 선택 처리"""
        self.selected_tol.set(terminal)
        # 모든 버튼 원래 색으로
        for btn in self.multi_tol_buttons.values():
            btn.configure(bg='SystemButtonFace')
        # 선택된 버튼만 노란색으로
        for btn_text, value in self.tol_values.items():
            if value == terminal:
                self.multi_tol_buttons[btn_text].configure(bg='yellow')

    def combine_cll_files(self):
        """Master와 Slave CLL 파일 병합"""
        try:
            # 선택된 서비스 확인
            selected_service = self.selected_service.get()
            if not selected_service:
                messagebox.showwarning("경고", "Service Name을 선택해주세요!")
                return

            def process_cll_file(file_path, start_row):
                try:
                    cll_df = pd.read_excel(file_path, header=4)
                    processed_data = []
                    row_count = start_row

                    # 선택된 서비스의 매핑 가져오기
                    service_mappings = self.stow_mapping.get(selected_service, [])

                    for idx, row in cll_df.iterrows():
                        if pd.notna(row['CNTR NO']):
                            # POD 값 가져오기
                            pod = str(row['POD']) if pd.notna(row['POD']) else ''
                            fpod = str(row['FDP']) if pd.notna(row['FDP']) else ''  # FPOD는 CLL의 FDP 값 사용
                            
                            # 초기값 설정
                            mapped_port = pod  # POD 초기값
                            mapped_stow = ''   # Stow 초기값
                            
                            # POD가 stow_code와 일치하는지 확인
                            for mapping in service_mappings:
                                if pod.upper() == mapping['stow_code'].upper():
                                    mapped_port = mapping['port']      # POD를 port 값으로 설정
                                    mapped_stow = mapping['stow_code'] # Stow를 stow_code 값으로 설정
                                    break

                            obl_row = {
                                'No': row_count,
                                'CtrNbr': row['CNTR NO'],
                                'ShOwn': 'N',
                                'Opr': 'MSC',
                                'POR': row['OPT'] if pd.notna(row['OPT']) else self.selected_pol.get(),
                                'POL': self.selected_pol.get(),
                                'TOL': self.selected_tol.get(),
                                'POD': mapped_port,
                                'TOD': '',
                                'Stow': mapped_stow,
                                'FPOD': fpod,  # FPOD는 원래 값 유지
                                'SzTp': int(row['T&S']) if pd.notna(row['T&S']) else '',
                                'Wgt': int(row['WGT']) if pd.notna(row['WGT']) else '',
                                'ForE': row['F/E'],
                                'Lbl': '',
                                'Rfopr': 'N',
                                'Rftemp': row['R/F'].replace(' CEL', '') if pd.notna(row['R/F']) else '',
                                'OvDH': row['OH'],
                                'OvDF': row['OL'] / 2 if pd.notna(row['OL']) and row['OL'] != 0 else '',
                                'OvDA': row['OL'] / 2 if pd.notna(row['OL']) and row['OL'] != 0 else '',
                                'OvDP': row['OW'] / 2 if pd.notna(row['OW']) and row['OW'] != 0 else '',
                                'OvDS': row['OW'] / 2 if pd.notna(row['OW']) and row['OW'] != 0 else '',
                                'OvSH': '',
                                'OvSF': '',
                                'OvSA': '',
                                'OvSP': '',
                                'OvSS': '',
                                'BL': '',
                                'HI': '',
                                'AC': '',
                                'Flip': '',
                                'Door': 'C',
                                'CustH': 'N',
                                'LenBB': '',
                                'BrthBB': '',
                                'HgtBB': '',
                                'WgtBB': '',
                                'Fumi': 'N',
                                'FuDt': '',
                                'VenDt': '',
                                'Venti': '',
                                'Damag': '',
                                'PPK': '',
                                'Food': '',
                                'Resi': '',
                                'Book': '',
                                'Cold': '',
                                'Catm': '',
                                'VGM': 'Y',
                                'VGM Weighting Method': '',
                                'HVC': '',
                                'BN1': '',
                                'BN2': '',
                                'BN3': '',
                                'BN4': '',
                                'Harmonised system codes': '',
                                'Description': '',
                                'Flexitank': '',
                                'UNNO': row['UNDG'],
                                'Class': row['IMDG'],
                                'PSN': '',
                                'N.Weight': '',
                                'S.Risk1': '',
                                'S.Risk2': '',
                                'S.Risk3': '',
                                'P.Group': '',
                                'LQ': '',
                                'EQ': '',
                                'FP': '',
                                'IMDG Remark': '',
                                'Sub Index': '',
                                'Inf type': '',
                                'Address': '',
                                'Street': '',
                                'City': '',
                                'Postal Code': '',
                                'Country Code': '',
                                'Country': '',
                                'Remark': ''
                            }
                            processed_data.append(obl_row)
                            row_count += 1
                    return processed_data
                except Exception as e:
                    raise Exception(f"파일 처리 중 오류 발생: {file_path}")

            # Master와 Slave 파일 처리
            master_data = process_cll_file(self.master_file, 1)
            slave_data = process_cll_file(self.slave_file, len(master_data) + 1)
            
            all_data = master_data + slave_data
            
            # DataFrame 생성 및 저장
            combined_df = pd.DataFrame(all_data)
            save_dir = os.path.dirname(self.master_file)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(save_dir, f"Combined_OBL_{timestamp}.xlsx")
            
            # 파일 저장
            combined_df.to_excel(output_file, index=False)
            
            # 결과 표시
            self.result_label.config(text=f"출력 파일: {output_file}")
            
            # 멀티 탭의 Summary만 업데이트
            self.update_multi_summary(combined_df)
            
            # 단일 탭의 Summary는 초기화
            if hasattr(self, 'single_summary_text'):
                self.single_summary_text.delete(1.0, tk.END)
                self.single_summary_text.insert(tk.END, "단일 CLL 탭에서 파일 변환 시 Summary가 표시됩니다.")
            
            messagebox.showinfo("성공", f"CLL 파일들이 성공적으로 병합되었습니다.\n총 {len(all_data)}개의 컨테이너가 처리되었습니다.")
            
        except Exception as e:
            print(f"Error in combine_cll_files: {str(e)}")  # 디버깅용
            messagebox.showerror("오류", str(e))

    def update_multi_summary(self, df):
        """병합된 CLL 파일들의 Container Summary 업데이트"""
        try:
            self.multi_summary_text.delete(1.0, tk.END)
            
            summary_text = "=== CLL 병합 Summary ===\n"
            summary_text += "================================\n\n"
            
            # 데이터프레임 유효성 검사
            if df is None or df.empty:
                raise ValueError("유효한 데이터가 없습니다.")
            
            # 컬럼 존재 여부 확인
            required_columns = ['SzTp', 'ForE', 'POD']
            for col in required_columns:
                if col not in df.columns:
                    raise ValueError(f"필요한 컬럼이 없습니다: {col}")
            
            # 데이터 처리
            total_containers = len(df)
            
            # 각 컬럼별 카운트 계산 (NaN 값 제외)
            size_type_counts = df['SzTp'].dropna().value_counts()
            full_empty_counts = df['ForE'].dropna().value_counts()
            pod_counts = df['POD'].dropna().value_counts()
            
            # Summary 텍스트 구성
            summary_text += f"Total Containers: {total_containers}\n"
            summary_text += "--------------------------------\n\n"
            
            summary_text += "=== Size Type Summary ===\n"
            for sz_tp, count in size_type_counts.items():
                if pd.notna(sz_tp):
                    summary_text += f"{sz_tp}: {count}\n"
            summary_text += "--------------------------------\n\n"
            
            summary_text += "=== Full/Empty Summary ===\n"
            for fe, count in full_empty_counts.items():
                if pd.notna(fe):
                    summary_text += f"{fe}: {count}\n"
            summary_text += "--------------------------------\n\n"
            
            summary_text += "=== POD Summary ===\n"
            for pod, count in pod_counts.items():
                if pd.notna(pod):
                    summary_text += f"{pod}: {count}\n"
            summary_text += "--------------------------------"
            
            self.multi_summary_text.insert(tk.END, summary_text)
            
        except Exception as e:
            self.multi_summary_text.delete(1.0, tk.END)
            self.multi_summary_text.insert(tk.END, f"Summary 생성 중 오류 발생: {str(e)}")

    def reset_all(self):
        """프로그램 상태 초기화"""
        # POL/TOL 버튼 초기화 (단일 탭)
        for btn in self.pol_buttons.values():
            btn.configure(bg='SystemButtonFace')
        for btn in self.tol_buttons.values():
            btn.configure(bg='SystemButtonFace')
        
        # POL/TOL 버튼 초기화 (멀티 탭)
        for btn in self.multi_pol_buttons.values():
            btn.configure(bg='SystemButtonFace')
        for btn in self.multi_tol_buttons.values():
            btn.configure(bg='SystemButtonFace')
        
        # 선택값 초기화
        self.selected_pol.set('')
        self.selected_tol.set('')
        
        # 파일 경로 레이블 초기화
        self.input_label.config(text="입력 파일: 없음")
        self.output_label.config(text="출력 파일: 없음")
        self.master_path_label.config(text="파일 경로: 없음")
        self.slave_path_label.config(text="파일 경로: 없음")
        self.result_label.config(text="출력 파일: 없음")
        
        # Summary 텍스트 초기화
        self.single_summary_text.delete(1.0, tk.END)
        self.single_summary_text.insert(tk.END, "단일 CLL 탭에서 파일 변환 시 Summary가 표시됩니다.")
        self.multi_summary_text.delete(1.0, tk.END)
        self.multi_summary_text.insert(tk.END, "Multi CLL 탭에서 파일 변환 시 Summary가 표시됩니다.")
        
        # 파일 관련 변수 초기화
        self.current_file = None
        self.output_file = None
        if hasattr(self, 'master_file'):
            delattr(self, 'master_file')
        if hasattr(self, 'slave_file'):
            delattr(self, 'slave_file')

        # Entry 위젯 초기화
        for pod_entry, sztp_entry, qty_entry in self.empty_entries:
            # Entry 위젯 상태 초기화
            pod_entry.delete(0, tk.END)
            sztp_entry.delete(0, tk.END)
            qty_entry.delete(0, tk.END)
            
            # 플레이스홀더 텍스트 설정
            pod_entry.insert(0, "POD")
            sztp_entry.insert(0, "SzTp")
            qty_entry.insert(0, "수량")
            
            # Entry 위젯 상태 설정
            pod_entry.config(state='normal')
            sztp_entry.config(state='normal')
            qty_entry.config(state='normal')

    def drop_itps_file(self, event):
        """ITPS 파일 드롭 처리"""
        file_path = event.data.strip('{}').strip('"')
        if not os.path.exists(file_path):
            messagebox.showerror("오류", "파일이 존재하지 않습니다.")
            return

        self.itps_file = file_path
        self.itps_input_label.config(text=f"ITPS 파일: {os.path.basename(file_path)}")
        self.itps_drop_label.config(text="ITPS 파일이 선택되었습니다")
        
        # 두 파일이 모두 선택되었다면 자동으로 처리 시작
        if self.itps_file and self.obl_file:
            self.process_itps_file()

    def drop_obl_for_itps(self, event):
        """ITPS 처리를 위한 OBL 파일 드롭 처리"""
        file_path = event.data.strip('{}').strip('"')
        if not os.path.exists(file_path):
            messagebox.showerror("오류", "파일이 존재하지 않습니다.")
            return

        self.obl_file = file_path
        self.itps_obl_label.config(text=f"OBL 파일: {os.path.basename(file_path)}")
        self.obl_drop_label.config(text="OBL 파일이 선택되었습니다")
        
        # 두 파일이 모두 선택되었다면 자동으로 처리 시작
        if self.itps_file and self.obl_file:
            self.process_itps_file()

    def process_itps_file(self):
        """ITPS 파일 처리 및 OBL에 추가"""
        try:
            # 선택된 서비스 확인
            selected_service = self.selected_service.get()
            if not selected_service:
                messagebox.showwarning("경고", "Service Name을 선택해주세요!")
                return

            # ITPS 파일 읽기 (헤더는 1행, 데이터는 3행부터)
            itps_df = pd.read_excel(self.itps_file, header=0, skiprows=[1])
            
            # OBL 파일 읽기
            obl_df = pd.read_excel(self.obl_file)
            
            # 기존 OBL의 마지막 No 값 가져오기
            last_no = obl_df['No'].max()
            
            # OBL의 POL과 TOL 값 가져오기
            obl_pol = obl_df['POL'].iloc[0] if not obl_df.empty else ''
            obl_tol = obl_df['TOL'].iloc[0] if not obl_df.empty else ''
            
            # 선택된 서비스의 매핑 가져오기
            service_mappings = self.stow_mapping.get(selected_service, [])
            
            # 기존 OBL 데이터에 대한 Stow Code 매핑 적용
            updated_obl_rows = []
            for _, row in obl_df.iterrows():
                obl_row = row.copy()
                pod = str(row['POD']) if pd.notna(row['POD']) else ''
                fpod = str(row['FPOD']) if pd.notna(row['FPOD']) else ''
                
                # POD가 stow_code와 일치하는지 확인
                mapped_port = pod
                mapped_stow = ''
                for mapping in service_mappings:
                    if pod.upper() == mapping['stow_code'].upper():
                        mapped_port = mapping['port']
                        mapped_stow = mapping['stow_code']
                        break
                
                obl_row['POD'] = mapped_port
                obl_row['Stow'] = mapped_stow
                obl_row['FPOD'] = fpod  # FPOD는 원래 값 유지
                updated_obl_rows.append(obl_row)
            
            # ITPS 데이터를 OBL 형식으로 변환
            new_rows = []
            for idx, row in itps_df.iterrows():
                try:
                    if pd.isna(row['Equipment Number']):
                        continue
                    
                    obl_row = {col: '' for col in obl_df.columns}
                    
                    # PORT CODE 변환 적용
                    por = self.convert_to_port_code(row['Origin Load Port']) if pd.notna(row['Origin Load Port']) else ''
                    pol = self.convert_to_port_code(obl_pol)  # OBL의 POL 사용
                    
                    # POD 값 가져오기
                    pod = str(row['Discharge Port']) if pd.notna(row['Discharge Port']) else ''
                    
                    # 초기값 설정
                    mapped_port = pod
                    mapped_stow = ''
                    
                    # POD가 stow_code와 일치하는지 확인
                    for mapping in service_mappings:
                        if pod.upper() == mapping['stow_code'].upper():
                            mapped_port = mapping['port']
                            mapped_stow = mapping['stow_code']
                            break
                    
                    # TpSZ 매핑 적용
                    tpsz = str(row['Type/Size']) if pd.notna(row['Type/Size']) else ''
                    mapped_tpsz = self.tpsz_mapping.get(tpsz, tpsz)
                    
                    # Rftemp 처리
                    rftemp = None
                    if pd.notna(row['Reefer Temp.']):
                        temp_str = str(row['Reefer Temp.']).split('/')[0].strip()
                        try:
                            rftemp = float(temp_str)
                        except ValueError:
                            rftemp = None
                    
                    # 나머지 필드 처리
                    obl_row.update({
                        'No': last_no + len(new_rows) + 1,
                        'CtrNbr': str(row['Equipment Number']) if pd.notna(row['Equipment Number']) else '',
                        'ShOwn': 'N',
                        'Opr': 'MSC',
                        'POR': por,
                        'POL': pol,
                        'TOL': obl_tol,
                        'POD': mapped_port,
                        'FPOD': pod,  # FPOD는 원래 값 유지
                        'Stow': mapped_stow,
                        'SzTp': mapped_tpsz,
                        'Wgt': int(row['Weight']) if pd.notna(row['Weight']) else '',
                        'ForE': str(row['Full/Empty']) if pd.notna(row['Full/Empty']) else 'N',
                        'Rfopr': 'N',
                        'Rftemp': f"{rftemp:.1f}" if rftemp is not None else '',
                        'Door': 'C',
                        'CustH': 'N',
                        'Fumi': 'N',
                        'VGM': 'Y',
                        'Class': str(int(row['IMO Class'])) if pd.notna(row['IMO Class']) and str(row['IMO Class']).replace('.', '').isdigit() else str(row['IMO Class']) if pd.notna(row['IMO Class']) else '',
                        'UNNO': str(row['UN Number'])[:6] if pd.notna(row['UN Number']) else ''
                    })
                    new_rows.append(obl_row)
                except Exception as e:
                    print(f"행 {idx} 데이터 확인 중 오류: {str(e)}")
                    continue
            
            # 기존 OBL 데이터와 새로운 ITPS 데이터 결합
            updated_obl_df = pd.DataFrame(updated_obl_rows)
            new_df = pd.DataFrame(new_rows)
            combined_df = pd.concat([updated_obl_df, new_df], ignore_index=True)
            
            # 모든 port 코드 변환 적용
            combined_df['POR'] = combined_df['POR'].apply(self.convert_to_port_code)
            combined_df['POL'] = combined_df['POL'].apply(self.convert_to_port_code)
            combined_df['POD'] = combined_df['POD'].apply(self.convert_to_port_code)
            combined_df['FPOD'] = combined_df['FPOD'].apply(self.convert_to_port_code)
            
            # 파일 저장
            save_dir = os.path.dirname(self.obl_file)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(save_dir, f"OBL_with_ITPS_{timestamp}.xlsx")
            combined_df.to_excel(output_file, index=False)
            
            # 결과 표시
            self.itps_output_label.config(text=f"출력 파일: {os.path.basename(output_file)}")
            
            # Summary 업데이트
            self.update_itps_summary(combined_df)
            
            messagebox.showinfo("성공", "ITPS 데이터가 성공적으로 추가되었습니다.")
            
        except Exception as e:
            messagebox.showerror("오류", f"ITPS 처리 중 오류 발생: {str(e)}")

    def update_itps_summary(self, df):
        """ITPS 처리 결과 Summary 업데이트"""
        try:
            self.itps_summary_text.delete(1.0, tk.END)
            
            summary_text = "=== ITPS 추가 결과 Summary ===\n"
            summary_text += "================================\n\n"
            
            # 전체 컨테이너 수
            total_containers = len(df)
            summary_text += f"전체 컨테이너 수: {total_containers}\n"
            summary_text += "--------------------------------\n\n"
            
            # F/E 별 통계
            fe_counts = df['ForE'].value_counts()
            summary_text += "=== Full/Empty 현황 ===\n"
            for fe, count in fe_counts.items():
                summary_text += f"{fe}: {count}개\n"
            summary_text += "--------------------------------\n\n"
            
            # Size Type 별 통계
            sztp_counts = df['SzTp'].value_counts()
            summary_text += "=== Size Type 현황 ===\n"
            for sztp, count in sztp_counts.items():
                if pd.notna(sztp):
                    summary_text += f"{sztp}: {count}개\n"
            summary_text += "--------------------------------\n\n"
            
            # POD 별 통계
            pod_counts = df['POD'].value_counts()
            summary_text += "=== POD 현황 ===\n"
            for pod, count in pod_counts.items():
                if pd.notna(pod):
                    summary_text += f"{pod}: {count}개\n"
            summary_text += "--------------------------------"
            
            self.itps_summary_text.insert(tk.END, summary_text)
            
        except Exception as e:
            self.itps_summary_text.delete(1.0, tk.END)
            self.itps_summary_text.insert(tk.END, f"Summary 생성 중 오류 발생: {str(e)}")

    def convert_to_port_code(self, port_name):
        """항구 이름을 5자리 PORT CODE로 변환"""
        if not port_name or pd.isna(port_name):
            return ''
            
        port_name = str(port_name).strip().upper()
        
        # 이미 5자리 코드인 경우 그대로 반환
        if len(port_name) == 5 and port_name.isalnum():
            return port_name
            
        # port_codes의 value(port name)와 매칭 시도
        for code, full_name in self.port_codes.items():
            if full_name == port_name:  # 정확한 매칭
                return code
            elif full_name in port_name or port_name in full_name:  # 부분 매칭
                return code
                
        # 매칭되는 코드가 없으면 원래 값 반환
        return port_name

    def drop_stowage_file(self, event):
        """Stowage Code 엑셀 파일 드롭 처리"""
        try:
            file_path = event.data.strip('{}').strip('"')
            if not os.path.exists(file_path):
                messagebox.showerror("오류", "파일이 존재하지 않습니다.")
                return

            # 엑셀 파일 읽기 (헤더는 2번째 행, 데이터는 3번째 행부터)
            df = pd.read_excel(file_path, header=1)
            
            # 매핑 딕셔너리 생성
            service_mappings = {}
            for _, row in df.iterrows():
                service_name = str(row['Service Name']).strip()
                stow_code = str(row['Stow Code OBL7']).strip()
                
                # Port 열에서 [ ] 안의 값 추출
                port_str = str(row['Port']).strip()
                port = ''
                if '[' in port_str and ']' in port_str:
                    start = port_str.find('[') + 1
                    end = port_str.find(']')
                    port = port_str[start:end].strip()
                
                if port and stow_code:  # port와 stow_code가 있는 경우만 매핑에 추가
                    if service_name not in service_mappings:
                        service_mappings[service_name] = []
                    service_mappings[service_name].append({
                        'port': port,
                        'stow_code': stow_code
                    })
            
            # 설정 저장
            self.stow_mapping = service_mappings
            
            # 엑셀 파일 경로 저장
            excel_dir = os.path.dirname(file_path)
            excel_name = os.path.splitext(os.path.basename(file_path))[0]
            self.stowage_config_file = os.path.join(excel_dir, f"{excel_name}_mapping.json")
            
            self.save_stowage_settings()
            
            # 미리보기 업데이트
            self.update_stowage_preview()
            
            messagebox.showinfo("성공", "Stowage Code 매핑이 성공적으로 업데이트되었습니다.")
            
        except Exception as e:
            messagebox.showerror("오류", f"파일 처리 중 오류가 발생했습니다: {str(e)}")

    def save_stowage_settings(self):
        """Stowage Code 설정 저장"""
        try:
            # JSON 파일로 저장
            with open(self.stowage_config_file, 'w', encoding='utf-8') as f:
                json.dump(self.stow_mapping, f, ensure_ascii=False, indent=2)
                
            messagebox.showinfo("성공", f"설정이 성공적으로 저장되었습니다.\n저장 위치: {self.stowage_config_file}")
            
        except Exception as e:
            messagebox.showerror("오류", f"설정 저장 중 오류가 발생했습니다: {str(e)}")

    def update_stowage_preview(self):
        """Stowage Code 매핑 미리보기 업데이트"""
        try:
            self.preview_text.delete(1.0, tk.END)
            
            # 서비스 목록 업데이트
            service_names = list(self.stow_mapping.keys())
            self.service_combo['values'] = service_names
            
            preview_text = "=== 현재 매핑 ===\n"
            selected_service = self.selected_service.get()
            
            if selected_service:
                preview_text += f"Service Name: {selected_service}\n"
                preview_text += "------------------------\n"
                
                # 선택된 서비스에 대한 매핑만 표시
                if selected_service in self.stow_mapping:
                    for mapping in self.stow_mapping[selected_service]:
                        preview_text += f"Port: {mapping['port']}\n"
                        preview_text += f"Stow Code: {mapping['stow_code']}\n"
                        preview_text += "------------------------\n"
            else:
                # 서비스가 선택되지 않은 경우 모든 매핑 표시
                for service_name, mappings in self.stow_mapping.items():
                    preview_text += f"Service Name: {service_name}\n"
                    for mapping in mappings:
                        preview_text += f"Port: {mapping['port']}\n"
                        preview_text += f"Stow Code: {mapping['stow_code']}\n"
                    preview_text += "------------------------\n"
                
            self.preview_text.insert(tk.END, preview_text)
            
        except Exception as e:
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, f"미리보기 업데이트 중 오류 발생: {str(e)}")

    def drop_tpsz_file(self, event):
        """TpSZ 엑셀 파일 드롭 처리"""
        try:
            file_path = event.data.strip('{}').strip('"')
            if not os.path.exists(file_path):
                messagebox.showerror("오류", "파일이 존재하지 않습니다.")
                return

            # 엑셀 파일 읽기
            df = pd.read_excel(file_path)
            
            # 컬럼 매핑 가져오기
            before_col = self.before_entry.get().strip()
            after_col = self.after_entry.get().strip()
            
            if not before_col or not after_col:
                messagebox.showerror("오류", "컬럼 매핑을 먼저 설정해주세요.")
                return
                
            if before_col not in df.columns or after_col not in df.columns:
                messagebox.showerror("오류", "설정한 컬럼명이 엑셀 파일에 존재하지 않습니다.")
                return

            # 매핑 딕셔너리 생성
            mapping = dict(zip(df[before_col], df[after_col]))
            
            # 설정 저장
            self.tpsz_mapping = mapping
            
            # JSON 파일 경로를 엑셀 파일과 동일한 디렉토리로 설정
            excel_dir = os.path.dirname(file_path)
            excel_name = os.path.splitext(os.path.basename(file_path))[0]
            self.tpsz_config_file = os.path.join(excel_dir, f"{excel_name}_mapping.json")
            
            self.save_tpsz_settings()
            
            # 미리보기 업데이트
            self.update_tpsz_preview()
            
            messagebox.showinfo("성공", "TpSZ 매핑이 성공적으로 업데이트되었습니다.")
            
        except Exception as e:
            messagebox.showerror("오류", f"파일 처리 중 오류가 발생했습니다: {str(e)}")

    def save_tpsz_settings(self):
        """TpSZ 설정 저장"""
        try:
            # 현재 설정 가져오기
            settings = {
                'column_mapping': {
                    'before': self.before_entry.get().strip(),
                    'after': self.after_entry.get().strip()
                },
                'mapping': self.tpsz_mapping
            }
            
            # JSON 파일로 저장
            with open(self.tpsz_config_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
                
            messagebox.showinfo("성공", f"설정이 성공적으로 저장되었습니다.\n저장 위치: {self.tpsz_config_file}")
            
        except Exception as e:
            messagebox.showerror("오류", f"설정 저장 중 오류가 발생했습니다: {str(e)}")

    def update_tpsz_preview(self):
        """TpSZ 매핑 미리보기 업데이트"""
        try:
            self.tpsz_preview_text.delete(1.0, tk.END)
            
            preview_text = "=== 컬럼 매핑 설정 ===\n"
            preview_text += f"Before 컬럼: {self.tpsz_column_mapping.get('before', '')}\n"
            preview_text += f"After 컬럼: {self.tpsz_column_mapping.get('after', '')}\n\n"
            
            preview_text += "=== 현재 매핑 ===\n"
            for before, after in self.tpsz_mapping.items():
                preview_text += f"{before}: {after}\n"
                
            self.tpsz_preview_text.insert(tk.END, preview_text)
            
        except Exception as e:
            self.tpsz_preview_text.delete(1.0, tk.END)
            self.tpsz_preview_text.insert(tk.END, f"미리보기 업데이트 중 오류 발생: {str(e)}")

    def setup_tpsz_tab(self):
        """TpSZ 관리 탭 설정"""
        # 메인 프레임
        main_frame = ttk.Frame(self.tpsz_tab)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 드래그 & 드롭 영역
        drop_frame = ttk.LabelFrame(main_frame, text="TpSZ 엑셀 파일")
        drop_frame.pack(fill="x", pady=(0, 10))

        self.tpsz_drop_label = ttk.Label(drop_frame, text="TpSZ 엑셀 파일을 여기에 드롭하세요")
        self.tpsz_drop_label.pack(pady=20)

        # 드래그 앤 드롭 바인딩
        self.tpsz_drop_label.drop_target_register(DND_FILES)
        self.tpsz_drop_label.dnd_bind('<<Drop>>', self.drop_tpsz_file)

        # 컬럼 매핑 설정 영역
        mapping_frame = ttk.LabelFrame(main_frame, text="컬럼 매핑 설정")
        mapping_frame.pack(fill="x", pady=(0, 10))

        # Before 컬럼 매핑
        before_frame = ttk.Frame(mapping_frame)
        before_frame.pack(fill="x", pady=5)
        ttk.Label(before_frame, text="Before 컬럼명:").pack(side="left", padx=5)
        self.before_entry = ttk.Entry(before_frame)
        self.before_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.before_entry.insert(0, self.tpsz_column_mapping.get('before', ''))

        # After 컬럼 매핑
        after_frame = ttk.Frame(mapping_frame)
        after_frame.pack(fill="x", pady=5)
        ttk.Label(after_frame, text="After 컬럼명:").pack(side="left", padx=5)
        self.after_entry = ttk.Entry(after_frame)
        self.after_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.after_entry.insert(0, self.tpsz_column_mapping.get('after', ''))

        # 저장 버튼
        save_button = ttk.Button(mapping_frame, text="설정 저장", command=self.save_tpsz_settings)
        save_button.pack(pady=10)

        # 현재 매핑 미리보기
        preview_frame = ttk.LabelFrame(main_frame, text="현재 매핑 미리보기")
        preview_frame.pack(fill="both", expand=True)
        
        self.tpsz_preview_text = tk.Text(preview_frame, height=10)
        self.tpsz_preview_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 현재 매핑 표시
        self.update_tpsz_preview()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ContainerConverter()
    app.run()

# test