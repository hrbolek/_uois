import dbInit


from DatabaseModel.myDevTools import *
from DatabaseModel import randomData
from DatabaseModel.models import PersonModel, LessonModel, StudentModel, ProgramModel, GroupModel, SubjectModel, SemesterModel, GroupTypeModel, LessonTypeModel, RoomModel, BuildingModel, AreaModel
#from DatabaseModel import sqlalchemyCore #přístup do modulu přes tečku


dbInit.InitAndRandomize()