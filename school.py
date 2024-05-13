from model import NsrEnhetApiModel
from osm import Node


transform_name = {
    'vgs': 'videregående skole',
    'VGS': 'videregående skole',
    'Vgs': 'videregående skole',
    'v.g.s.': 'videregående skole',
    'V.g.s.': 'videregående skole',
    'KVS': 'kristen videregående skole',
    'Kvs': 'kristen videregående skole',
    'Videregående': 'videregående',
    'Vidaregåande': 'vidaregåande',
    'Videregåande': 'vidaregåande',
    'Vidregående': 'videregående',
    'Vidregåande': 'vidaregåande',
    'Bibelskole': 'bibelskole',
    'Oppvekstsenter': 'oppvekstsenter',
    'Oppvekstområde': 'oppvekstområde',
    'Oppveksttun': 'oppveksttun',
    'Oppvekst': 'oppvekstsenter',
    'oppvekst': 'oppvekstsenter',
    'Oahppogald': 'oahppogald',
    'Grunnskoleundervisning': 'grunnskoleundervisning',
    'Grunnskolen': 'grunnskolen',
    'Grunnskole': 'grunnskole',
    'Grunnskoler': 'grunnskoler',
    'Grunnskole/adm': 'grunnskole',
    'Privatskole': 'privatskole',
    'Privatskule': 'privatskule',
    'Private': 'private',
    'Skolen': 'skolen',
    'Skoler': 'skolen',
    'Skole': 'skole',
    'Skule': 'skule',
    'Skuvle': 'skuvle',
    'Skuvla': 'skuvla',
    'Grunn-': 'grunn-',
    'Barne-': 'barne-',
    'Barne-Og': 'barne- og',
    'Barn': 'barn',
    'Ungdomsskole': 'ungdomsskole',
    'Ungdomsskule': 'ungdomsskule',
    'Undomsskule': 'ungdomsskule',
    'Ungdomssskole': 'ungdomsskole',
    'Ungdomstrinn': 'ungdomstrinn',
    'Ungdomstrinnet': 'ungdomstrinnet',
    'Ungdom': 'ungdomsskole',
    'Nærmiljøskole': 'nærmiljøskole',
    'Friskole': 'friskole',
    'Friskule': 'friskule',
    'Sentralskole': 'sentralskole',
    'Sentralskule': 'sentralskule',
    'Grendaskole': 'grendaskole',
    'Reindriftsskole': 'reindriftsskole',
    'Voksenopplæring': 'voksenopplæring',
    'Morsmålsopplæring': 'morsmålsopplæring',
    'Opplæring': 'opplæring',
    '10-Årige': '10-årige',
    'Utdanning': 'utdanning',
    'Kultursenter': 'kultursenter',
    'Kultur': 'kultur',
    'Flerbrukssenter': 'flerbrukssenter',
    'Kristne': 'kristne',
    'Skolesenter': 'skolesenter',
    'Læringssenter': 'læringssenter',
    'Senter': 'senter',
    'Fengsel': 'fengsel',
    'Tospråklig': 'tospråklig',
    'Flerspråklige': 'flerspråklige',
    'Alternative': 'alternative',
    'Tekniske': 'tekniske',
    'Maritime': 'maritime',
    'Offshore': 'offshore',
    'Omegn': 'omegn',
    'Åbarneskole': 'Å barneskole',
    'lurøy': 'Lurøy',
    'hasselvika': 'Hasselvika',
    'tjeldsund': 'Tjeldsund',
    'Kfskolen': 'KFskolen',
    'Davinvi': 'daVinci',
    'masi': 'Masi',
    'Rkk': 'RKK',
    'Aib': 'AIB',
    '(ais)': '(AIS)',
    'Awt': 'AWT',
    'Abr': 'ABR',
    'Fpg': 'FPG',
    'Oks': 'OKS',
    'De': 'de',
    'Cs': 'CS',
    'Ii': 'II',
    'S': 'skole',
    'St': 'St.',
    'Of': 'of',
    'Foreningen': '',
    'Skolelag': '',
    'Stiftelsen': '',
    'stiftelsen': '',
    'Stiftinga': '',
    'Studiested': '',
    'Skolested': '',
    'Avdeling': '',
    'Avd': '',
    'Avd.': '',
    'avd.': '',
    'AS': '',
    'As': '',
    'SA': '',
    'Sa': '',
    'BA': '',
    'Ba': '',
    'ANS': '',
    'Ans': ''
}

transform_names = {
    ' og Barnehage': '',
    ' og barnehage': '',
    ' og Sfo': '',
    'Montessori skole': 'Montessoriskole',
    'oppvekstsenter skole': 'oppvekstsenter',
    'oppvekstsenter skule': 'oppvekstsenter',
    'Nordre Land kommune, ': '',
    'Salangen kommune, ': '',
    'Kvs-': 'Kristen videregående skole ',
    'Smi-': 'SMI-',
    'Ntg': 'NTG'
}

transform_operator = {
    'Sa': 'SA',
    'Vgs': 'vgs',
    'Suohkan': 'suohkan',
    'Gielda': 'gielda',
    'Tjïelte': 'tjïelte',
    'Tjielte': 'tjielte',
    'Oks': 'OKS'
}


def tag_name(node: Node, school: NsrEnhetApiModel) -> None:
    """Fix school name"""

    name = school.name
    original_name = name

    name = name.replace("/", " / ")

    if school.characteristic:
        original_name += ", " + school.characteristic
        if (school.characteristic.lower() not in
                ["skole", "skule", "skolen", "skulen", "avd skule", "avd skole", "avd undervisning", "avdeling skole", "avdeling skule"]):
            name += ", " + school.characteristic

    if name == name.upper():
        name = name.title()

    name_split = name.split()
    name = ""
    for word in name_split:
        if word[-1] == ",":
            word_without_comma = word[:-1]
        else:
            word_without_comma = word

        if word_without_comma in transform_name:
            if transform_name[word_without_comma]:
                name += transform_name[word_without_comma]
        else:
            name += word

        if word[-1] == ",":
            name += ", "
        else:
            name += " "

    for words in transform_names:
        name = name.replace(words, transform_names[words])

    name = name[0].upper() + name[1:].replace(" ,", ",").replace(",,", ",").replace("  ", " ").strip("- ")

    #            if school['Maalform'] == "Nynorsk":
    #                name = name.replace("skole", "skule").replace("videregående", "vidaregåande")

    node.tags["name"] = name
    if name != original_name:
        node.tags["ORIGINAL_NAME"] = original_name


def tag_telephone(node: Node, school: NsrEnhetApiModel) -> None:
    if not school.telephone:
        return

    phone = school.telephone.replace("  ", " ")
    if not phone:
        return

    if phone[0] != "+":
        if phone[0:2] == "00":
            phone = "+" + phone[2:].lstrip()
        else:
            phone = "+47 " + phone
    node.tags["phone"] = phone


def tag_grade_and_isced(node: Node, school: NsrEnhetApiModel):
    isced = ""
    grade1 = ""
    grade2 = ""

    if school.grade_gs_from and school.grade_gs_to:
        grade1 = school.grade_gs_from
        grade2 = school.grade_gs_to

    if school.grade_vgs_from and school.grade_vgs_to:
        if not grade1:
            grade1 = school.grade_vgs_from
        grade2 = school.grade_vgs_to

    if grade1 and grade2:
        if grade1 == grade2:
            node.tags["grades"] = str(grade1)
        else:
            node.tags["grades"] = str(grade1) + "-" + str(grade2)

        if grade1 <= 7:
            isced = "1"
        if grade1 <= 10 and grade2 >= 8:
            isced += ";2"
        if grade1 >= 11 or grade2 >= 11:
            isced += ";3"

    if not isced:
        if school.is_primary_education:
            isced = "1;2"
        if school.is_secondary_education:
            isced += ";3"

    node.tags["isced:level"] = isced.strip(";")


def tag_metadata(node: Node, school: NsrEnhetApiModel) -> None:
    if school.date_created:
        node.tags["DATE_CREATED"] = school.date_created.strftime("%Y-%m-%d")

    if school.date_changed:
        node.tags["DATE_UPDATED"] = school.date_changed.strftime("%Y-%m-%d")

    if school.municipality.name:
        node.tags["MUNICIPALITY"] = school.municipality.name

    if school.county.name:
        node.tags["COUNTY"] = school.county.name

    if school.characteristic:
        node.tags["DEPARTMENT"] = school.characteristic

    if school.written_language.name:
        node.tags["LANGUAGE"] = school.written_language.name

    if school.business_codes:
        node.tags["ENTITY_CODES"] = "; ".join([f"{code.priority}.{code.name}" for code in school.business_codes])

    if school.school_categories:
        node.tags["SCHOOL_CODES"] = str("; ".join([code.name for code in school.school_categories]))

    if school.is_special_school:
        node.tags["SPECIAL_NEEDS"] = "Spesialskole"

    if school.coordinate.geo_source:
        node.tags["LOCATION_SOURCE"] = school.coordinate.geo_source


def tag_address(node: Node, school: NsrEnhetApiModel) -> None:
    address = school.location_address
    if address:
        address_line = ""
        if address.address and (address.address != "-"):
            address_line = address.address + ", "
        if address.post_code:
            address_line += address.post_code + " "
        if address.city:
            address_line += address.city
        if address.country and address.country != "Norge":
            address_line += ", " + address.country
        if address_line:
            node.tags["ADDRESS"] = address_line


def tag_operator(node: Node, school: NsrEnhetApiModel) -> None:
    for parent in school.parent_relations:
        if parent.relation_type.id == "1" and parent.unit.name:  # Owner

            operator_split = parent.unit.name.split()
            operator = ""
            for word in operator_split:
                if word in transform_operator:
                    if transform_operator[word]:
                        operator += transform_operator[word] + " "
                else:
                    operator += word + " "

            operator = operator[0].upper() + operator[1:].replace("  ", " ").strip()
            node.tags["operator"] = operator


def tag_operator_type(node: Node, school: NsrEnhetApiModel) -> None:
    if school.is_public_school:
        node.tags["operator:type"] = "public"
        node.tags["fee"] = "no"
    elif school.is_private_school:
        node.tags["operator:type"] = "private"
        node.tags["fee"] = "yes"


def create_school_node(school: NsrEnhetApiModel) -> Node:
    node = Node(lat=school.coordinate.latitude, lon=school.coordinate.longitude)
    if not (school.coordinate.longitude and school.coordinate.latitude):
        node.tags["GEOCODE"] = "yes"

    node.tags["amenity"] = "school"
    node.tags["ref:udir_nsr"] = school.org_num
    tag_name(node, school)

    if school.email:
        node.tags["email"] = school.email.lower()  # TODO: Do lower() formatting in model

    if school.url and not("@" in school.url):
        node.tags["website"] = "https://" + school.url.lstrip("/").replace("www2.", "").replace("www.", "").replace(" ","")

    tag_telephone(node, school)

    if school.num_pupils:
        node.tags["capacity"] = str(school.num_pupils)

    tag_grade_and_isced(node, school)

    # Check for "Andre tjenester tilknyttet undervisning" code
    if any([code.code == "85.609" for code in school.business_codes]):
        node.tags["OTHER_SERVICES"] = "yes"

    # Get operator
    tag_operator_type(node, school)
    tag_operator(node, school)

    tag_metadata(node, school)

    tag_address(node, school)

    return node
