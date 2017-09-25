import random
from datetime import date

from django.conf import settings

from faker import Factory
from oauth2_provider.models import Application

from services.celerytasks.events import update_event
from services.celerytasks.institutes import update_institue
from services.departments.models import Course, Department, DepartmentCourse, Facility
from services.events.models import Events
from services.feeds.models import Feed
from services.institutes.models import Institute, InstituteDepartment, InstituteFacility, InstituteType
from services.utils.tasks import add_feed
from users.models import UserProfile, UserRole

start_date = date.today().replace(day=1, month=1, year=1979).toordinal()
end_date = date.today().replace(day=1, month=1, year=2009).toordinal()

event_start_date = date.today().replace(day=1, month=1, year=2016).toordinal()
event_end_date = date.today().replace(day=1, month=12, year=2016).toordinal()
join_end_date = date.today().replace(day=1, month=8, year=2016).toordinal()

fake = Factory.create()


class PopulateDumyData(object):

    def create_superuser(self):
        self.superadmin = UserProfile.objects.create_superuser("admin@in.com", "admin")
        print("Created Super user")

    def create_application(self):
        app = Application.objects.filter(name="Myinstitute").first()
        if not app:
            app = Application(
                client_type=Application.CLIENT_PUBLIC, name="Myinstitute", user=self.superadmin,
                authorization_grant_type=Application.GRANT_PASSWORD,
                client_id=settings.CLIENT_ID,
                client_secret=settings.CLIENT_SECRET)  # noqa
            app.save()
        return app

    def addUsers(self):
        role = UserRole.objects.get(name='student')
        users_objs = []
        for i in range(50):
            print('.',)
            users_objs.append(UserProfile(first_name='student' + '_' + str(i),
                                          last_name='student' + '_' + str(i),
                                          email='student_' + str(i) + '@student.com',
                                          user_role=role,
                                          date_of_birth=date.fromordinal(random.randint(start_date, end_date)),
                                          gender=random.randrange(1, 3)
                                          ))
        print('student set created',)
        role = UserRole.objects.get(name='teacher')
        for i in range(50):
            print('.',)
            users_objs.append(UserProfile(first_name='teacher' + '_' + str(i),
                                          last_name='teacher' + '_' + str(i),
                                          email='teacher' + str(i) + '@teacher.com',
                                          user_role=role,
                                          date_of_birth=date.fromordinal(random.randint(start_date, end_date)),
                                          gender=random.randrange(1, 3)
                                          ))
        print('teacher set created',)
        role = UserRole.objects.get(name='principle')
        for i in range(50):
            print('.',)
            users_objs.append(UserProfile(first_name='principle' + '_' + str(i),
                                          last_name='principle' + '_' + str(i),
                                          email='principle' + str(i) + '@principle.com',
                                          user_role=role,
                                          date_of_birth=date.fromordinal(random.randint(start_date, end_date)),
                                          gender=random.randrange(1, 3)
                                          ))
        print('principle set created',)
        role = UserRole.objects.get(name='other')
        for i in range(50):
            print('.',)
            users_objs.append(UserProfile(first_name='other' + '_' + str(i),
                                          last_name='other' + '_' + str(i),
                                          email='other' + str(i) + '@other.com',
                                          user_role=role,
                                          date_of_birth=date.fromordinal(random.randint(start_date, end_date)),
                                          gender=random.randrange(1, 3)
                                          ))

        print('other set created',)
        UserProfile.objects.bulk_create(users_objs)
        print('user done',)

    def addUserPassword(self):
        for user in UserProfile.objects.filter(is_superuser=False):
            print('.',)
            user.set_password('123')
            user.save()

    def addInstitutes(self):
        institute_type = InstituteType.objects.get(name='university')
        board_type = InstituteType.objects.get(name='board')
        school_type = InstituteType.objects.get(name='school')
        tuition_type = InstituteType.objects.get(name='tuition')
        branch_type = InstituteType.objects.get(name='branch')
        institute_objs = []
        for i in range(50):
            print('.',)
            institute_objs.append(Institute(name='university' + '_' + str(i),
                                            institute_type=institute_type,
                                            established_date=date.fromordinal(random.randint(start_date, end_date))
                                            )
                                  )
        print('university set created',)
        Institute.objects.bulk_create(institute_objs)
        institute_objs = []
        for i in range(50):
            print('.',)
            institute_objs.append(Institute(name='board' + '_' + str(i),
                                            institute_type=board_type,
                                            established_date=date.fromordinal(random.randint(start_date, end_date))
                                            )
                                  )
        print('board set created',)
        Institute.objects.bulk_create(institute_objs)
        institute_objs = []
        for obj in Institute.objects.filter(institute_type=board_type):
            for i in range(20):
                print('.',)
                institute_objs.append(Institute(name=obj.name + '_school' + '_' + str(i),
                                                institute_type=school_type, parent=obj,
                                                established_date=date.fromordinal(random.randint(start_date, end_date))
                                            )
                                      )
        print('_school set created',)
        Institute.objects.bulk_create(institute_objs)
        institute_objs = []
        for i in range(50):
            print('.',)
            institute_objs.append(Institute(name='tuition' + '_' + str(i),
                                            institute_type=tuition_type))
        print('tuition set created',)
        Institute.objects.bulk_create(institute_objs)
        institute_objs = []
        for obj in Institute.objects.filter(institute_type=tuition_type):
            for i in range(20):
                print('.',)
                institute_objs.append(Institute(name=obj.name + '_branch' + '_' + str(i),
                                                institute_type=branch_type,
                                                parent=obj,
                                                established_date=date.fromordinal(random.randint(start_date, end_date))
                                            )
                                      )
        print('_branch set created',)
        Institute.objects.bulk_create(institute_objs)
        print('Institute created done.',)

    def addRole(self):
        role_name = ['student', 'teacher', 'principle', 'other']
        role_obj = []
        for role in  role_name:
            print('.',)
            role_obj.append(UserRole(name=role))
        UserRole.objects.bulk_create(role_obj)
        print("Role created",)

    def addEvents(self):
        events_obj = []
        for ins in Institute.objects.all()[:50]:
            print('.',)
            for depart in InstituteDepartment.objects.filter(institute=ins):
                print('.',)
                events_obj.append(Events(institute=ins,
                                         department=depart.department,
                                         apply_date=date.fromordinal(random.randint(event_start_date, event_end_date)),
                                         apply_last_date=date.fromordinal(random.randint(event_start_date, event_end_date)),
                                         event_start_date=date.fromordinal(random.randint(join_end_date, event_end_date)),
                                         event_last_date=date.fromordinal(random.randint(join_end_date, event_end_date)),
                                         availability=random.randrange(10, 1000),
                                         name='event_' + str(ins.name) + '_' + str(depart.department.name),
                                         tags=['event_' + str(ins.name) + '_' + str(depart.department.name)]
                                         ))
        Events.objects.bulk_create(events_obj)
        print("Events created",)

    def addInstituteType(self):
        inst_type_list = ['university', 'board', 'school', 'institute', 'tuition', 'branch']
        objs = []
        for inst_type in inst_type_list:
            print('.',)
            objs.append(InstituteType(name=inst_type))
        InstituteType.objects.bulk_create(objs)
        print('addInstituteType done',)

    def addCourse(self):
        objs = []
        for i in range(10):
            print('.',)
            objs.append(Course(name='course' + str(i), start_year=2000 + i, end_year=2010 + i))
        Course.objects.bulk_create(objs)
        print('addCourse done',)

    def addFacility(self):
        objs = []
        for i in range(10):
            print('.',)
            objs.append(Facility(name='facility' + str(i)))
        Facility.objects.bulk_create(objs)
        print('addFacility done',)

    def addDepartment(self):
        objs = []
        for i in range(10):
            print('.',)
            objs.append(Department(name='department' + str(i), is_lab=True if i % 5 == 0 else False))
        Department.objects.bulk_create(objs)
        print('addDepartment done',)

    def addDepartmentCourse(self):
        objs = []
        for dep in Department.objects.all():
            print('.',)
            for obj in Course.objects.all():
                objs.append(DepartmentCourse(department=dep, course=obj))
        DepartmentCourse.objects.bulk_create(objs)
        print('addDepartmentCourse done',)

    def addInstituteDepartment(self):
        objs = []
        for ins in Institute.objects.all()[:30]:
            print('.',)
            for dep in Department.objects.all():
                objs.append(InstituteDepartment(institute=ins, department=dep))
        InstituteDepartment.objects.bulk_create(objs)
        print('addInstituteDepartment done',)

    def addInstituteFacility(self):
        objs = []
        for ins in Institute.objects.all()[:30]:
            print('.',)
            for fac in Facility.objects.all():
                objs.append(InstituteFacility(institute=ins, facility=fac))
        InstituteFacility.objects.bulk_create(objs)
        print('addInstituteFacility done',)

    def addFeed(self):
        add_feed()

    def addInstituteAddress(self):
        print("Adding Address to every institute will take time more then 15 mins",)
        count = 0
        for inst in  Institute.objects.all():
            if count != 40:
                inst.address = {'raw': fake.street_name(),
                                'street_number': fake.random_digit(),
                                'route': fake.word(),
                                'locality': fake.word(),
                                'postal_code': fake.postalcode(),
                                'state': fake.state(),
                                'state_code': fake.state_abbr(),
                                'country': fake.country(),
                                'country_code': fake.country_code()
                              }
                inst.save()
            else:
                yn = input("We have added address to 40 institute. more it will take 10 mins, Do you want to continue? y/n")
                if yn != 'y':
                    print('done')
                    break
            count += 1

    def addUserAddress(self):
        print("Adding Address to every User will take time more then 15 mins",)
        count = 0
        for user in  UserProfile.objects.all():
            if count != 50:
                user.address = {'raw': fake.street_name(),
                                'street_number': fake.random_digit(),
                                'route': fake.word(),
                                'locality': fake.word(),
                                'postal_code': fake.postalcode(),
                                'state': fake.state(),
                                'state_code': fake.state_abbr(),
                                'country': fake.country(),
                                'country_code': fake.country_code()
                              }
                user.save()
            else:
                yn = input("We have added address to 50 users. more it will take 10 mins, Do you want to continue? y/n")
                if yn != 'y':
                    print('done')
                    break
            count += 1

    def update_total_feed_count(self):
        for feed in Feed.objects.all().distinct('object_id'):
            content_object = feed.content_object
            content_object.total_feed = Feed.objects.filter(object_id=feed.content_object.id).count()
            print('.',)
            content_object.save()

    def update_institute_for_mongo(self):
        for obj in Institute.objects.all():
            print('.',)
            update_institue.delay(str(obj.id))

    def update_event_for_mongo(self):
        for obj in Events.objects.all():
            print('.',)
            update_event.delay(str(obj.id))

    def loadDummyData(self):
        print("It will take few minutes to set-up dummy data to run project")
        self.create_superuser()
        self.create_application()
        self.addRole()
        self.addUsers()
        self.addUserPassword()
        self.addInstituteType()
        self.addInstitutes()
        self.addCourse()
        self.addFacility()
        self.addDepartment()
        self.addDepartmentCourse()
        self.addInstituteDepartment()
        self.addEvents()
        self.addFeed()
        self.addInstituteAddress()
        self.addUserAddress()
        self.update_total_feed_count()
        self.update_institute_for_mongo()
