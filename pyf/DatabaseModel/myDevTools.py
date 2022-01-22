
def AddToSessionAndCommit(object, session):
    session.add(object)
    session.commit()

def AddToSession(object, session):
    session.add(object)

def CommitSession(session):
    session.commit()

def CloseSession(session):
    session.close()
