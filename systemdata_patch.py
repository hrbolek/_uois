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
    # c1803533-fdab-46a3-a45c-f2caaff8d24f
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

event_id = "a1d59525-d774-4109-9f94-d5ff458f3c67"
event = {
    "id": event_id,
    "name": "zkouška",
    "startdate": "2024-07-10T08:00:00",
    "enddate": "2024-07-10T12:00:00"
}

def patch_classifications(data, classifications):    
    events = data.get("events", [])
    existing_event = next((x for x in events if x.get("id", None) == event_id), None)
    if not existing_event:
        events.append(event)

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
        item["event_id"] = event_id

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

# def create_finance(data, **props):
#     # c1803533-fdab-46a3-a45c-f2caaff8d24f
    
#     result = {
#         "id": new_id(),
#         **props,
#         "_chunk": 10,
#         "name": "finance",
#         "description": "finance",
#         "finance_type_id": "3ffbc624-fe29-4486-9a56-3bc6a4e5b576"
#     }
#     return result

# def patch_projects(data, projects):
#     pass

def patch_classifications_2(data, classifications):
    data["acclassificationplans"] = data.get("acclassificationplans", [])
    def create_exam(**props):
        exam = {
            "id": new_id(),
            **props
        }
        data["acclassificationplans"].append(exam)
        return exam
        

    semesters = {}
    for item in classifications:
        semester_id = item.get("semester_id", None)
        if semester_id is None:
            continue
        if semester_id not in semesters:
            semester = next((x for x in data.get("acsemesters", []) if x.get("id", None) == semester_id), None)
            if semester is None:
                continue
            semesters[semester_id] = semester
        else:
            semester = semesters[semester_id]
        
        rbacobject_id = item.get("rbacobject_id", None)
        if rbacobject_id is not None:
            continue
        
        semester_rbacobject_id = semester.get("rbacobject_id", None)
        item["rbacobject_id"] = semester_rbacobject_id

    for key, value in semesters.items():
        exam_id = value.get("exam_id", None)
        if exam_id is not None:
            continue
        exam = create_exam(semester_id=key, rbacobject_id=value.get("rbacobject_id", None))
        exam_id = exam.get("id", None)
        value["exam_id"] = exam_id
        # print(f"semester {key} rbacobject_id {value.get('rbacobject_id', None)}")

    for item in classifications:
        semester_id = item.get("semester_id", None)
        if semester_id is None:
            continue

        semester = semesters.get(semester_id, None)
        if semester is None:
            continue
        
        exam_id = semester.get("exam_id", None)
        item["exam_id"] = exam_id

    return classifications
    pass

def patch_plan(data, plans):
    result = data.get("acplans", [])
    data["plans"] = result
    return plans

def patch_plan_lessons(data, plan_lessons):
    "plan_lessons"
    result = data.get("acplanitems", [])
    data["plan_lessons"] = result
    return plan_lessons

def patch_invitations(data, invitations):
    # "event_invitations"
    result = data.get("event_users", [])
    if result:
        return invitations

    classifications = data.get("classifications", [])
    for item in classifications:
        student_id = item.get("student_id", None)
        student = next((x for x in data.get("acprograms_students", []) if x.get("student_id", None) == student_id), None)
        if student is None:
            continue
        user_id = student.get("user_id", None)
        if user_id is None:
            continue
        invitation = next((x for x in result if x.get("user_id", None) == user_id and x.get("event_id", None) == event_id), None)
        if invitation is None:
            continue
        invitation = {
            "id": f"{new_id()}",
            "user_id": user_id,
            "event_id": event_id,
            "state_id": "d7c38ef9-c7d0-4ff9-a72e-fd1e0b70f387"
        }
        invitations.append(invitation)
        
    return invitations

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

    classifications = data.get("acclassifications", [])
    classifications = patch_classifications_2(data, classifications)
    data["acclassifications"] = classifications

    patchn_invitations = data.get("event_users", [])
    patchn_invitations = patch_invitations(data, patchn_invitations)
    data["event_invitations"] = patchn_invitations


    return data


def update_chunks(data):
    result_data = {}
    dbModels = list(data.keys())

    for model in dbModels:
        rows = data.get(model, [])

        # vsechny radky do dict
        rowsdict = {}
        for asdict in rows:
            row_id = asdict.get("id", None)
            if row_id is None:
                continue
            rowsdict[row_id] = asdict

        # vsechny primarni klice do ids
        ids = set(rowsdict.keys())
        done = set()
        chunk_id = 0

        while len(done) < len(ids):
            todo = set()

            for row in rowsdict.values():
                row_id = row.get("id", None)
                if row_id in done:
                    continue

                skip_this_id = False
                for key, value in row.items():
                    if key == "id":
                        continue
                    if key == "rbacobject_id":
                        continue

                    if value is None:
                        continue
                    if not isinstance(value, str):
                        continue
                    if value not in ids:
                        continue
                    if value not in done:
                        skip_this_id = True
                        break

                if skip_this_id:
                    continue

                row["_chunk"] = chunk_id
                todo.add(row_id)

            print(f"{model} chunk {chunk_id} todo/done/all {len(todo)}/{len(done)}/{len(ids)}")

            if len(todo) == 0:
                remaining = ids - done
                raise ValueError(
                    f"Cyklus nebo nevyresitelna zavislost v modelu '{model}', remaining ids: {sorted(remaining)[:10]}{'...' if len(remaining) > 10 else ''  }"
                )

            done = done.union(todo)
            chunk_id += 1

        result_data[model] = list(rowsdict.values())

    return result_data

def main():
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    data = patch_data(data)
    result_data = update_chunks(data)
    with open(f"{filename}.txt", "w", encoding="utf-8") as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)

main()