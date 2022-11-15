# create relations request - sections
# sectiosns is phases of request stuedent, student-teacher, teacher-approver

data = {
    'request0':{
        'id':'',
        'creator_id':'',
        'strartTime': {
            'date': '',
            'time': ''
        },
        'endTime': {
            'date': '',
            'time': ''
        },
        'name':'vacation',
        'detailRequest':{
            'sections':[
                {
                    'id':'',
                    'startTime': {
                        'date': '',
                        'time': ''
                    },
                    'endTime': {
                        'date': '',
                        'time': ''
                    },
                    'name' : 'STUDENT',
                    'value': 'p1'
                },

                {
                    'id':'',
                    'startTime': {
                        'date': '',
                        'time': ''
                    },
                    'endTime': {
                        'date': '',
                        'time': ''
                    },
                    'name' : 'STUDENT-TEACHER',
                    'value': 'p12'
                },
                {
                    'id':'',
                    'startTime': {
                        'date': '',
                        'time': ''
                    },
                    'endTime': {
                        'date': '',
                        'time': ''
                    },
                    'name' : 'TEACHER-DEAN',
                    'value': 'p23'
                }    
            ], 
            'parts':[
                {
                    'PART1': {
                        'STUDENT':{
                            'name' : '',
                            'group' : '',
                            'program': ''
                        },
                        'REQUEST':{
                            'description': ''
                        }
                        
                    }
                },

                {
                    'PART2': {
                        'TEACHER':{
                            'name' : '',
                            'nameDepartment' : 'K209',
                        },
                        'SUGGESTION':{
                            'description': ''
                        }
                        
                    }
                },

                {
                    'PART3': {
                        'DEAN':{
                            'name' : ''
                        },
                        'SUGGESTION':{
                            'description': ''
                        }

                    }
                }
            ]
        }
    }

}
