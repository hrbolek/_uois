import { Link, useParams } from "react-router-dom";
import { useEffect, useState, useMemo } from "react";

import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { root } from '../../helpers/index';
import { useQueryGQL, Loading, LoadingError } from '../../helpers/index';
import { Provider } from 'react-redux'
import { useSelector } from 'react-redux'
import { configureStore } from '@reduxjs/toolkit'
import { groupSlice } from './groupstorage'

/**
 * Retrieves the data from GraphQL API endpoint
 * @param {*} id - identificator
 * @function
 */
 export const UniversityLargeQuery = (id) => 
 fetch('/gql', {
     method: 'POST',
     headers: {
         'Content-Type': 'application/json',
     },
     cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
     redirect: 'follow', // manual, *follow, error
     body: JSON.stringify({
         "query":
             `query ($id: UUID!) {
                groupById(id: $id) {
                  id
                  name
                  roles {
                    roletype {
                      name
                    }
                    user {
                      name
                      surname
                      email
                    }
                  }
                  mastergroup {
                    id
                    name
                    grouptype {
                      name
                    }
                    mastergroup {
                      id
                      name
                      grouptype {
                        name
                      }
                    }
                    mastergroup {
                      id
                      name
                      grouptype {
                        name
                      }
                    }
                  }
                }
              }`,
         "variables": {"id": id}
     }),
 })

/**
 * Retrieves the data from GraphQL API endpoint
 * @param {*} id - identificator
 * @function
 */
 export const DepartmentLargeQuery = (id) => 
 fetch('/gql', {
     method: 'POST',
     headers: {
         'Content-Type': 'application/json',
     },
     cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
     redirect: 'follow', // manual, *follow, error
     body: JSON.stringify({
         "query":
             `query ($id: UUID!) {
                groupById(id: $id) {
                  id
                  name
                  roles {
                    roletype {
                      name
                    }
                    user {
                      name
                      surname
                      email
                    }
                  }
                  memberships {
                    user {
                      id
                      name
                      surname
                      email
                    }
                  }
                  mastergroup {
                    id
                    name
                    grouptype {
                      name
                    }
                    mastergroup {
                      id
                      name
                      grouptype {
                        name
                      }
                      mastergroup {
                        id
                        name
                        grouptype {
                          name
                        }
                      }
                    }
                  }
                }
              }`,
         "variables": {"id": id}
     }),
 })

export const UniversityLargeStoryBook = (props) => {
    const extraProps = {
        "id": "4e3b3503-5d20-458b-9f4d-fd7f35306ee0",
        "name": "University of IT",
        "roles": [
          {
            "roletype": {
              "name": "rector"
            },
            "user": {
              "name": "Marie Václav",
              "surname": "Černý",
              "email": "Marie.Václav.Černý@university.world"
            }
          },
          {
            "roletype": {
              "name": "vicerector"
            },
            "user": {
              "name": "Pavel Jan",
              "surname": "Černý",
              "email": "Pavel.Jan.Černý@university.world"
            }
          },
          {
            "roletype": {
              "name": "vicerector"
            },
            "user": {
              "name": "Eva Václav",
              "surname": "Dvořák",
              "email": "Eva.Václav.Dvořák@university.world"
            }
          },
          {
            "roletype": {
              "name": "vicerector"
            },
            "user": {
              "name": "Hana Milan",
              "surname": "Nováková",
              "email": "Hana.Milan.Nováková@university.world"
            }
          },
          {
            "roletype": {
              "name": "vicerector"
            },
            "user": {
              "name": "Miroslav Věra",
              "surname": "Pokorná",
              "email": "Miroslav.Věra.Pokorná@university.world"
            }
          }
        ],
        "mastergroup": null
      }
    return (
        <div>{JSON.stringify(props)}</div>
    )
}

export const DepartmentLargeStoryBook = (props) => {
    const extraProps = {
        "id": "6a5d4172-a557-4637-8d83-96baaf2bd79a",
        "name": "Department 1-1",
        "roles": [
          {
            "roletype": {
              "name": "head of department"
            },
            "user": {
              "name": "Pavel Jakub",
              "surname": "Němcová",
              "email": "Pavel.Jakub.Němcová@university.world"
            }
          }
        ],
        "memberships": [
          {
            "user": {
              "id": "3edba4da-d136-42d8-9f65-2e63e3e9d3f4",
              "name": "Lenka Pavel",
              "surname": "Novotná",
              "email": "Lenka.Pavel.Novotná@university.world"
            }
          },
          {
            "user": {
              "id": "4184c7fd-3ea2-4be4-9f2f-ac4f9d99209c",
              "name": "Miroslav Kateřina",
              "surname": "Procházková",
              "email": "Miroslav.Kateřina.Procházková@university.world"
            }
          },
          {
            "user": {
              "id": "cbf2ef40-3beb-40df-83dd-8e82e2b99d42",
              "name": "Josef Marie",
              "surname": "Dvořák",
              "email": "Josef.Marie.Dvořák@university.world"
            }
          },
          {
            "user": {
              "id": "04847541-5bce-410b-ae75-93f0f35e2865",
              "name": "Pavel Miroslav",
              "surname": "Veselý",
              "email": "Pavel.Miroslav.Veselý@university.world"
            }
          },
          {
            "user": {
              "id": "514bc096-f18b-4be6-addc-8f15830e7979",
              "name": "Pavel Jakub",
              "surname": "Němcová",
              "email": "Pavel.Jakub.Němcová@university.world"
            }
          },
          {
            "user": {
              "id": "f393db40-de3c-4f82-bc74-ff7c9ec7f8da",
              "name": "Petr Milan",
              "surname": "Němcová",
              "email": "Petr.Milan.Němcová@university.world"
            }
          },
          {
            "user": {
              "id": "2fa9bcad-0091-4045-93d0-7c37a50d7020",
              "name": "Jana Milan",
              "surname": "Dvořáková",
              "email": "Jana.Milan.Dvořáková@university.world"
            }
          },
          {
            "user": {
              "id": "c772be6b-1094-48bc-a12d-9105ef9be64d",
              "name": "Zdeněk Anna",
              "surname": "Krejčí",
              "email": "Zdeněk.Anna.Krejčí@university.world"
            }
          },
          {
            "user": {
              "id": "2d1745b1-d99f-44cf-9629-ef26c7c06c09",
              "name": "Věra Lucie",
              "surname": "Dvořák",
              "email": "Věra.Lucie.Dvořák@university.world"
            }
          },
          {
            "user": {
              "id": "3a9bac44-0c0d-4084-9555-042ed34fbc0e",
              "name": "Lucie Eva",
              "surname": "Kučerová",
              "email": "Lucie.Eva.Kučerová@university.world"
            }
          },
          {
            "user": {
              "id": "a27b5e36-a5b3-4237-999e-a86794aa1a9e",
              "name": "Hana Petr",
              "surname": "Horák",
              "email": "Hana.Petr.Horák@university.world"
            }
          },
          {
            "user": {
              "id": "a989321d-fe26-4819-b048-6e8928afeab9",
              "name": "Lucie Miroslav",
              "surname": "Černý",
              "email": "Lucie.Miroslav.Černý@university.world"
            }
          },
          {
            "user": {
              "id": "ac96892d-96ac-4380-bfb1-992e1f6233c2",
              "name": "Jana Kateřina",
              "surname": "Němec",
              "email": "Jana.Kateřina.Němec@university.world"
            }
          },
          {
            "user": {
              "id": "4f93e71b-0af2-48d6-97e5-4bedd525e140",
              "name": "Tomáš Alena",
              "surname": "Horáková",
              "email": "Tomáš.Alena.Horáková@university.world"
            }
          },
          {
            "user": {
              "id": "61d57844-c09d-4488-bbc5-29c6c0882cf5",
              "name": "Jaroslav Jan",
              "surname": "Černý",
              "email": "Jaroslav.Jan.Černý@university.world"
            }
          },
          {
            "user": {
              "id": "3f6719ad-7328-451a-8265-8ca05a67d459",
              "name": "Miroslav Pavel",
              "surname": "Dvořák",
              "email": "Miroslav.Pavel.Dvořák@university.world"
            }
          },
          {
            "user": {
              "id": "c4729a41-6a13-4ffa-b2fa-32aba0cc068b",
              "name": "Eva Milan",
              "surname": "Horáková",
              "email": "Eva.Milan.Horáková@university.world"
            }
          },
          {
            "user": {
              "id": "96474762-2766-4a58-8764-6cf96d2dbe29",
              "name": "Tomáš František",
              "surname": "Veselý",
              "email": "Tomáš.František.Veselý@university.world"
            }
          }
        ],
        "mastergroup": {
          "id": "8685d00b-cb75-4c3a-a7b8-ad4ca48d8026",
          "name": "Faculty 1",
          "grouptype": {
            "name": "faculty"
          },
          "mastergroup": {
            "id": "4e3b3503-5d20-458b-9f4d-fd7f35306ee0",
            "name": "University of IT",
            "grouptype": {
              "name": "university"
            },
            "mastergroup": null
          }
        }
      }
    return (
        <div>{JSON.stringify(props)}</div>
    )
}


/**
 * Fetch the data from API endpoint and renders a page representing a department
 * @param {*} props - extra props for encapsulated components / visualisers
 * @param {*} [props.as = DepartmentLargeStoryBook] - ReactJS component (function) which is responsible for rendering
 * @param {*} [props.with = DepartmentLargeQuery] - function fetching the data and returning promise with the data from API endpoint
 * @function
 */
 export const DepartmentLargeFetching = (props) => {

    const Visualizer = props.as || DepartmentLargeStoryBook;
    const queryFunc = props.with || DepartmentLargeQuery;

    const [state, error] = useQueryGQL(props.id, queryFunc, (response) => response.data.group, [props.id])
    
    if (error != null) {
        return <LoadingError error={error} />
    } else if (state != null) {
        return <Visualizer {...props} {...state} />
    } else {
        return <Loading>Katedra {props.id}</Loading>
    }
}

export const DepartmentPage = (props) => {
    const { id } = useParams();

    return (
        <DepartmentLargeFetching {...props} id={id} />
    )       
}

export const DepartmentLargeStore = (props) => {
    const group = useSelector((state) => state.group)
    return (
        <DepartmentLargeStoryBook {...group} />
    )
}

export const DepartmentPageWithStore = (props) => {
    const { id } = useParams();

    const createStore = useMemo(() =>{
        configureStore({ reducer: groupSlice.reducer })
    }, [id])

    return (
        <Provider store={createStore}>
            <DepartmentLargeFetching {...props} id={id} />
        </Provider>
    )       
}