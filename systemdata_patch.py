from functools import cache
import json
from pathlib import Path
import uuid



filename = "systemdata.hk2025.json"
filename = Path(__file__).parent / "systemdata.hk2025.json"

collections_cache = {}
def find(data, collection_name, id):
    @cache
    def find_in(id):
        item = next((x for x in data.get(collection_name, []) if x.get("id", None) == id), None)
        return item
    
    if collection_name not in collections_cache:
        collections_cache[collection_name] = find_in
        
    finder = collections_cache[collection_name]
    return finder(id)

def find_program(data, id):
    return find(data, "acprograms", id)

def new_id():
    return str(uuid.uuid4())

def createRbacObjectId(data, **props):
    groups = data.get("groups", [])
    rbacobject_id = new_id
    rbac = {
        "id": rbacobject_id,
        **props,
        "_chunk": 10,
        "name": "rbacobject",
        "description": "rbacobject",
        "grouptype_id": "3ffbc624-fe29-4486-9a56-3bc6a4e5b576"
    }
    groups.append(rbac)
    id = rbac.get("id", None)
    return id

def patch_programs(data, programs):
    for item in programs:
        guarantors_group_id = item.get("guarantors_group_id", None)
        licenced_group_id = item.get("licenced_group_id", None)
        if licenced_group_id is None:
            continue
        # rbacobject_id = item.get("rbacobject_id") or createRbacObjectId(data, mastergroup_id=licenced_group_id)
        if guarantors_group_id is None:
            guarantors_group_id = new_id()
            data["groups"].append({
                "id": guarantors_group_id,
                "rbacobject_id": guarantors_group_id,
                "mastergroup_id": licenced_group_id,
                "grouptype_id": "b1bedec8-931f-11ed-9b95-0242ac110002",
                "name": f"garanti studijního programu {item.get('name', '')}",
            })
        # item["rbacobject_id"] = rbacobject_id
        item["guarantors_group_id"] = guarantors_group_id
        item["rbacobject_id"] = guarantors_group_id
    return programs

def patch_students(data, students):
    for item in students:
        student_id = item.get("student_id", None)
        item["user_id"] = student_id
        program_id = item.get("program_id", None)
        if program_id is None:
            continue
        program = find_program(data, program_id)
        if program is None:
            continue
        rbacobject_id = program.get("rbacobject_id", None)
        item["rbacobject_id"] = rbacobject_id
        item["semester_number"] = item.get("semester_number", 1)
    return students




def patch_subjects(data, subjects):
    for item in subjects:
        guarantors_group_id = item.get("guarantors_group_id", None)
        program_id = item.get("program_id", None)
        if program_id is None:
            continue
        program = find_program(data, program_id)
        if program is None:
            continue
        program_guarantors_group_id = program.get("guarantors_group_id", None)
        # rbacobject_id = item.get("rbacobject_id") or createRbacObjectId(data, mastergroup_id=program_guarantors_group_id)
        if guarantors_group_id is None:
            guarantors_group_id = new_id()
            data["groups"].append({
                "id": guarantors_group_id,
                "rbacobject_id": guarantors_group_id,
                "mastergroup_id": program_guarantors_group_id,
                "name": f"garanti předmětu {item.get('name', '')}",
            })
        
        # item["rbacobject_id"] = rbacobject_id
        item["guarantors_group_id"] = guarantors_group_id
    return subjects

def patch_semesters(data, semesters):
    for item in semesters:
        
        subject_id = item.get("subject_id", None)
        if subject_id is None:
            continue
        rbacobject_id = item.get("rbacobject_id", None)
        if rbacobject_id is not None:
            continue
        subject = next((x for x in data.get("acsubjects", []) if x.get("id", None) == subject_id), None)
        if subject is None:
            continue
        subject_rbacobject_id = subject.get("rbacobject_id", None)
        item["rbacobject_id"] = subject_rbacobject_id        
    return semesters

def patch_plans(data, plans):
    for item in plans:
        
        semester_id = item.get("semester_id", None)
        if semester_id is None:
            continue
        rbacobject_id = item.get("rbacobject_id", None)
        if rbacobject_id is not None:
            continue
        semester = next((x for x in data.get("acsemesters", []) if x.get("id", None) == semester_id), None)
        if semester is None:
            continue
        semester_rbacobject_id = semester.get("rbacobject_id", None)
        item["rbacobject_id"] = semester_rbacobject_id        
    return plans

def patch_plan_lessons(data, plan_lessons):
    for item in plan_lessons:
        
        plan_id = item.get("plan_id", None)
        if plan_id is None:
            continue
        rbacobject_id = item.get("rbacobject_id", None)
        if rbacobject_id is not None:
            continue
        plan = next((x for x in data.get("acplans", []) if x.get("id", None) == plan_id), None)
        if plan is None:
            continue
        plan_rbacobject_id = plan.get("rbacobject_id", None)
        item["rbacobject_id"] = plan_rbacobject_id        
    return plan_lessons

def patch_classifications(data, classifications):
    for item in classifications:
        
        semester_id = item.get("semester_id", None)
        if semester_id is None:
            continue
        rbacobject_id = item.get("rbacobject_id", None)
        if rbacobject_id is not None:
            continue
        semester = next((x for x in data.get("acsemesters", []) if x.get("id", None) == semester_id), None)
        if semester is None:
            continue
        semester_rbacobject_id = semester.get("rbacobject_id", None)
        item["rbacobject_id"] = semester_rbacobject_id        

        student_id = item.get("student_id", None)
        student = next((x for x in data.get("acprograms_students", []) if x.get("student_id", None) == student_id), None)
        if student:
            item["student_id"] = student.get("id", None)

    return classifications

def patch_topics(data, topics):
    for item in topics:
        
        semester_id = item.get("semester_id", None)
        if semester_id is None:
            continue
        rbacobject_id = item.get("rbacobject_id", None)
        if rbacobject_id is not None:
            continue
        semester = next((x for x in data.get("acsemesters", []) if x.get("id", None) == semester_id), None)
        if semester is None:
            continue
        semester_rbacobject_id = semester.get("rbacobject_id", None)
        item["rbacobject_id"] = semester_rbacobject_id        
    return topics

def patch_lessons(data, lessons):
    for item in lessons:
        
        topic_id = item.get("topic_id", None)
        if topic_id is None:
            continue
        rbacobject_id = item.get("rbacobject_id", None)
        if rbacobject_id is not None:
            continue
        topic = next((x for x in data.get("actopics", []) if x.get("id", None) == topic_id), None)
        if topic is None:
            continue
        topic_rbacobject_id = topic.get("rbacobject_id", None)
        item["rbacobject_id"] = topic_rbacobject_id        
    return lessons

def patch_groups(data, groups):
    for item in groups:
        id = item.get("id", None)
        rbacobject_id = item.get("rbacobject_id", None)
        if rbacobject_id is None:
            item["rbacobject_id"] = id
    return groups

def patch_users(data, users):
    for item in users:
        id = item.get("id", None)
        rbacobject_id = item.get("rbacobject_id", None)
        if rbacobject_id is None:
            item["rbacobject_id"] = id
    return users

def patch_data(data):
    groups = data.get("groups", [])
    groups = patch_groups(data, groups)
    data["groups"] = groups

    users = data.get("users", [])
    users = patch_users(data, users)
    data["users"] = users

    programs = data.get("acprograms", [])
    programs = patch_programs(data, programs)
    data["acprograms"] = programs

    students = data.get("acprograms_students", [])
    students = patch_students(data, students)
    data["acprograms_students"] = students

    subjects = data.get("acsubjects", [])
    subjects = patch_subjects(data, subjects)
    data["acsubjects"] = subjects

    semesters = data.get("acsemesters", [])
    semesters = patch_semesters(data, semesters)
    data["acsemesters"] = semesters

    classifications = data.get("acclassifications", [])
    classifications = patch_classifications(data, classifications)
    data["acclassifications"] = classifications

    topics = data.get("actopics", [])
    topics = patch_topics(data, topics)
    data["actopics"] = topics

    lessons = data.get("aclessons", [])
    lessons = patch_lessons(data, lessons)
    data["aclessons"] = lessons

    plans = data.get("plans", [])
    plans = patch_plans(data, plans)
    data["plans"] = plans

    plan_lessons = data.get("plan_lessons", [])
    plan_lessons = patch_plan_lessons(data, plan_lessons)
    data["plan_lessons"] = plan_lessons
    return data


def main():
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    data = patch_data(data)

    with open(f"{filename}.txt", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

main()