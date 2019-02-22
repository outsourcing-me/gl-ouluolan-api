import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType, utils
from . import models
from graphene_file_upload.scalars import Upload


class BaseConnection(relay.Connection):

    class Meta:
        abstract = True

    total_count = graphene.Int()

    @staticmethod
    def resolve_total_count(self, info):
        return self.length


class Department(SQLAlchemyObjectType):

    class Meta:
        model = models.Department
        interfaces = (relay.Node, )


class DepartmentConnection__(BaseConnection):

    class Meta:
        node = Department


class Employee(SQLAlchemyObjectType):

    class Meta:
        model = models.Employee
        interfaces = (relay.Node, )


class EmployeeConnection__(BaseConnection):

    class Meta:
        node = Employee


class Role(SQLAlchemyObjectType):

    class Meta:
        model = models.Role
        interfaces = (relay.Node, )


class RoleConnection__(BaseConnection):

    class Meta:
        node = Role


SortEnumEmployee = utils.sort_enum_for_model(models.Employee, 'SortEnumEmployee',
                                             lambda c, d: c.upper() + ('_ASC' if d else '_DESC'))


class UploadMutation(graphene.Mutation):

    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()

    def mutate(self, info, file, **kwargs):
        # do something with your file

        return UploadMutation(success=True)


class MyMutations(graphene.ObjectType):
    upload_file = UploadMutation.Field()


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    employee = graphene.Field(Employee, name=graphene.String())

    def resolve_employee(self, info, **args):
        query = Employee.get_query(info)
        return query.filter_by(name=args['name']).first()
    # Allow only single column sorting
    all_employees = SQLAlchemyConnectionField(
        EmployeeConnection__,
        sort=graphene.Argument(
            SortEnumEmployee,
            default_value=utils.EnumValue('id_asc', models.Employee.id.asc())))
    # Allows sorting over multiple columns, by default over the primary key
    all_roles = SQLAlchemyConnectionField(RoleConnection__)
    # Disable sorting over this field
    all_departments = SQLAlchemyConnectionField(
        DepartmentConnection__, sort=None)


schema = graphene.Schema(query=Query, mutation=MyMutations, types=[
                         Department, Employee, Role])
