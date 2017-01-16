import os

import asyncio

import aiohttp
from aiohttp_swagger import setup_swagger
from chilero.web import init
from chilero.pg import Application, Resource


class Employee(Resource):
    table_name = 'employees'
    allowed_fields = ['name']
    required_fields = ['name']

    def serialize_list_object(self, row):
        """Serializes the object for list response (collection url)"""
        return dict(
            id=row[0],
            name=row[2],
            url=self.get_object_url(row[0])
        )

    def serialize_object(self, row):
        """Serializes the object for detailed response (entity url)"""
        return dict(
            id=row[0],
            organization=self.get_object_url(row[1], 'organization'),
            name=row[2],
            url=self.get_object_url(row[0])
        )

    @asyncio.coroutine
    def index(self, organization_id):
        """
        ---
        description: Lists all employees of an organization
        tags:
        - Employees
        produces:
        - application/json
        parameters:
        - name: organization_id
          required: true
          type: integer
          in: path
        responses:
            "200":
                description: successful operation. Return the list of all employees of the organization
        """
        conditions = dict(organizationid=organization_id)
        index = yield from self.do_index(conditions=conditions)
        return self.response(index)

    def show(self, *args, **kwargs):
        """
        ---
        description: Loads an employee entity
        tags:
        - Employees
        produces:
        - application/json
        parameters:
        - name: organization_id
          required: true
          type: integer
          in: path
        - name: id
          required: true
          type: integer
          in: path
        responses:
            "200":
                description: successful operation.
        """
        return super(Employee, self).show(*args, **kwargs)

    def new(self, *args, **kwargs):
        """
        ---
        description: Creates an employee
        tags:
        - Employees
        produces:
        - application/json
        parameters:
        - name: organization_id
          required: true
          type: integer
          in: path
        - name: payload
          required: true
          type: string
          in: body
          default: '{"name": ""}'
        responses:
            "200":
                description: successful operation.
        """
        return super(Employee, self).new(*args, **kwargs)

    def destroy(self, *args, **kwargs):
        """
        ---
        description: Deletes an employee
        tags:
        - Employees
        produces:
        - application/json
        parameters:
        - name: organization_id
          required: true
          type: integer
          in: path
        - name: id
          required: true
          type: integer
          in: path
        responses:
            "200":
                description: successful operation.
        """
        return super(Employee, self).destroy(*args, **kwargs)

    def default_kwargs_for_urls(self):
        return dict(
            organization_id=self.request.match_info.get('organization_id')
        )

    def default_data(self, data):
        data['organizationid'] = self.request.match_info.get('organization_id')
        return data

    def prepare_insert(self, data):
        return self.default_data(data)

    def prepare_update(self, data):
        return self.default_data(data)


class Organization(Resource):
    table_name = 'organizations'
    allowed_fields = ['name']
    required_fields = ['name']

    nested_entity_resources = dict(
        employees=Employee
    )

    def serialize_object(self, row):
        return dict(
            id=row[0],
            name=row[1],
            url=self.get_object_url(row[0])
        )

    def index(self):
        """
        ---
        description: Lists all organizations
        tags:
        - Organizations
        produces:
        - application/json
        responses:
            "200":
                description: successful operation. Return the list of all organizations
        """
        return super(Organization, self).index()

    def show(self, *args, **kwargs):
        """
        ---
        description: Loads an organization entity
        tags:
        - Organizations
        produces:
        - application/json
        parameters:
        - name: id
          required: true
          type: integer
          in: path
        responses:
            "200":
                description: successful operation.
        """
        return super(Organization, self).show(*args, **kwargs)

    def new(self, *args, **kwargs):
        """
        ---
        description: Creates an organization
        tags:
        - Organizations
        produces:
        - application/json
        parameters:
        - name: payload
          required: true
          type: string
          in: body
          default: '{"name": ""}'
        responses:
            "200":
                description: successful operation.
        """
        return super(Organization, self).new(*args, **kwargs)

    def destroy(self, *args, **kwargs):
        """
        ---
        description: Deletes an organization
        tags:
        - Organizations
        produces:
        - application/json
        parameters:
        - name: id
          required: true
          type: integer
          in: path
        responses:
            "200":
                description: successful operation.
        """
        return super(Organization, self).destroy(*args, **kwargs)


def main():
    routes = [
        ['/api/v1/organizations', Organization]
    ]

    settings = dict(
        db_url=os.getenv(
            'DATABASE_URL', 'postgresql://postgres@localhost:5432/org'
        )
    )

    app = init(Application, routes=routes, settings=settings)

    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8000))

    setup_swagger(
        app,
        description='Sample Organization Management API Service',
        api_version='0.0.1',
        title='Organization Management API',
    )

    aiohttp.web.run_app(app, port=PORT, host=HOST)


if __name__ == '__main__':
    main()