from django.contrib.auth import get_user_model
from ninja import Router, Status
from .schemas import UserOut, UserMessage

router = Router(tags=["Accounts"])
User = get_user_model()


@router.get("", response=list[UserOut])
def list_users(
    request,
    role: str | None = None,
    q: str | None = None,
):
    """
    Menampilkan daftar akun/pengguna (maksimal 100).
    Dapat difilter berdasarkan role (ADMIN, TEACHER, STUDENT) atau query username.
    """
    qs = User.objects.all().order_by("id")
    if role:
        qs = qs.filter(role=role.upper())
    if q:
        qs = qs.filter(username__icontains=q)
    return qs[:100]


@router.get("/teachers", response=list[UserOut])
def list_teachers(request):
    """
    Menampilkan daftar dosen (role TEACHER).
    Gunakan ID akun di sini sebagai teacher_id pada Course.
    """
    return User.objects.filter(role="TEACHER").order_by("id")


@router.get("/{user_id}", response={200: UserOut, 404: UserMessage})
def get_user(request, user_id: int):
    """
    Menampilkan informasi profil akun berdasarkan user_id.
    """
    user = User.objects.filter(pk=user_id).first()
    if user is None:
        return Status(404, {"detail": "User tidak ditemukan"})
    return Status(200, user)