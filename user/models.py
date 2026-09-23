from django.db import models
from company.models import Company, FiscalYear
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# ---------------- USER MANAGER ---------------- #
class UserAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        """Creates and returns a user with the given email and username."""
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")
        email                                   = self.normalize_email(email)
        company                                 = extra_fields.get("company") or create_demo_company()
        extra_fields["company"]                 = company
        user                                    = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,username,password,*args,**kwargs):
        company                                 = create_demo_company()
        user                                    = self.create_user(
        email                                   = self.normalize_email(email),
        username                                = username,
        password                                = password,
        company                                 = company,
        )
        user.is_admin                           = True
        user.is_staff                           = True
        user.is_superuser                       = True
        user.company_admin                      = True
        user.branch_admin                       = True
        user.save(using=self._db)
        contentTypes                            = ContentType.objects.all()
        user.contenttypes.set(contentTypes)
        permissions                             = Permission.objects.values_list('id',flat=True).all()
        permissionLists                         = list(permissions)
        user.user_permissions.set(permissionLists)
        return user
    
# ---------------- DEFAULT DEMO COMPANY CREATION ---------------- #
def create_demo_company():
    fiscal_year                                 = FiscalYear.objects.first()
    company, created                            = Company.objects.get_or_create(
        name                                    = "Demo Company",
        defaults = {
            'fiscal_year'                       : fiscal_year,
            "print_name"                        : "Demo Pvt. Ltd.",
            "fiscal_year_beginning_from"        : "2081-04-01",
            "book_commencing_from"              : "2080-04-01",
            "address"                           : "Buddhanagar, Kathmandu",
            "pan"                               : "123456789",
            "phone"                             : "+977-9800000000",
            "email"                             : "demo@company.com",
        },
    )
    if created:
        print("Default demo company created successfully!")
    else:
        print("Default demo company already exists.")
    return company

# ---------------- ROLE MODEL ---------------- #

class Roles(models.Model):
    name                                        = models.CharField(max_length=100, null=True, blank=True)
    code                                        = models.CharField(max_length=100, null=True, blank=True)
    is_active                                   = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    
class Meta:
    db_table                                    = 'roles'  
    verbose_name                                = 'Role'  
    verbose_name_plural                         = 'Roles' 
    ordering                                    = ['name']

# ---------------- USER MODEL ---------------- #
class User(AbstractBaseUser, PermissionsMixin):
    email                                       = models.EmailField(verbose_name="Email Address", max_length=100, unique=True)
    username                                    = models.CharField(verbose_name="User Name", max_length=100, unique=True)
    english_fullname                            = models.CharField(verbose_name="User Full Name in English", max_length=100, null=True, blank=True)
    profile_image                               = models.ImageField(upload_to="images/profiles/", null=True, blank=True)
    last_login                                  = models.DateTimeField(verbose_name="Last Login", auto_now=True, null=True)
    is_admin                                    = models.BooleanField(default=False)
    is_active                                   = models.BooleanField(default=True)
    is_staff                                    = models.BooleanField(default=False)
    company                                     = models.ForeignKey(Company, on_delete=models.PROTECT)
    role                                        = models.ManyToManyField(Roles, blank=True)
    company_admin                               = models.BooleanField(default=False)
    is_employee                                 = models.BooleanField(default=False)
    contenttypes                                = models.ManyToManyField(ContentType, blank=True, related_name="user_permissions")
    objects                                     = UserAccountManager()
    USERNAME_FIELD                              = "email"
    REQUIRED_FIELDS                             = ["username","password"] 
    device_id                                   = models.CharField(max_length=255, null=True, blank=True)
    otp_code                                    = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at                              = models.DateTimeField(null=True, blank=True)
    created_at                                  = models.DateTimeField(auto_now_add=True)
    updated_at                                  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        return super().has_module_perms(app_label)

    @property
    def userImageURL(self):
        """Safely returns the URL of the profile image."""
        return self.profile_image.url if self.profile_image else ""

    def reset_password(self, old_password, new_password):
      if self.check_password(old_password):
          self.set_password(new_password)
          self.save()
          return True
      return False
    
class Meta:
    db_table                                    = 'user_account'  
    verbose_name                                = 'User'  
    verbose_name_plural                         = 'Users' 
    ordering                                    = ['created_at']  
    permissions = [
        ('view_user', 'Can view user'),
        ('edit_user', 'Can edit user'),
        ('delete_user', 'Can delete user'),
    ]