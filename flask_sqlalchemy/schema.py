import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Department as DepartmentModel, Employee as EmployeeModel, User as UserModel
from datetime import datetime
import secrets

#Types
class DepartmentType(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel

class EmployeeType(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeModel

class UserType(SQLAlchemyObjectType):
    class Meta:
        model = UserModel




#Queries
class Query(graphene.ObjectType):
    employees = graphene.List(EmployeeType)
    departments = graphene.List(DepartmentType)
    users = graphene.List(UserType)
    search = graphene.List(EmployeeType, filter=graphene.String())

    def resolve_employees(self, info, *args, **kwargs):
        return EmployeeModel.query.all()

    def resolve_departments(self, info,*args, **kwargs):
        return DepartmentModel.query.all()

    def resolve_users(self, info, *args, **kwargs):
        return UserModel.query.all()

    def resolve_search(self, info, filter, **kwargs):
        employees = db_session.query(EmployeeModel).filter(EmployeeModel.name.like('%' + filter +'%')).all()
        return employees

#Mutations

class CreateDepartment(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()

    class Arguments:
        name = graphene.String()

    def mutate(self, info, name):
        newDepartment = DepartmentModel(name=name)
        db_session.add(newDepartment)
        db_session.commit()

        return CreateDepartment(
            id = newDepartment.id,
            name = newDepartment.name
        )

class CreateEmployee(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    hiredOn = graphene.String()
    departmentid = graphene.Int()

    class Arguments:
        name = graphene.String()
        hiredOn = graphene.String()
        departmentid = graphene.Int()

    def mutate(self, info, name, hiredOn, departmentid):
        print('----------------------------------------')
        print(info.context.headers['Authorization'])
        print('----------------------------------------')
        hiredDate = datetime.strptime(hiredOn, '%d/%m/%Y')
        newEmployee = EmployeeModel(name=name, hired_on=hiredDate, department_id=departmentid)
        db_session.add(newEmployee)
        db_session.commit()

        return CreateEmployee(
            id = newEmployee.id,
            name = newEmployee.name,
            hiredOn = newEmployee.hired_on,
            departmentid = newEmployee.department_id
        )

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()

    class Arguments:
        name = graphene.String()
        email = graphene.String()
        password = graphene.String()

    def mutate(self, info, name, email, password):
        newUser = UserModel(name=name, email=email, password=password)
        db_session.add(newUser)
        db_session.commit()

        token = secrets.token_hex(24)
        return CreateUser(user=newUser, token=token)

class DeleteUser(graphene.Mutation):
    deleteId = graphene.Int()

    class Arguments:
        deleteId = graphene.Int()

    def mutate(self, info, deleteId):

        deleteUser = db_session.query(UserModel).filter(UserModel.id == deleteId).one()
        db_session.delete(deleteUser)
        db_session.commit()

        return DeleteUser(deleteId = deleteId)

class Login(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()

    class Arguments:
        email = graphene.String()
        password = graphene.String()

    def mutate(self, info, email, password):
        user = None
        userFound = False
        try:
            user = db_session.query(UserModel).filter(UserModel.email == email).filter(UserModel.password == password).one()
            userFound = True
        except:
            userFound = False

        token = secrets.token_hex(24) if userFound else ''

        return Login(user=user, token = token)


class Mutation(graphene.ObjectType):
    create_department = CreateDepartment.Field()
    create_employee = CreateEmployee.Field()
    create_user = CreateUser.Field()
    delete_user = DeleteUser.Field()
    login = Login.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
