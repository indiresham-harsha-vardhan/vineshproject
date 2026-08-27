from django.db import models
from django.utils.text import slugify


class PropertyType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="property_types/",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Example: fa-solid fa-car"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Property(models.Model):

    STATUS_CHOICES = [
        ("available", "Available"),
        ("sold", "Sold"),
        ("reserved", "Reserved"),
        ("under_construction", "Under Construction"),
        ("coming_soon", "Coming Soon"),
        ("not_available", "Not Available"),
    ]

    PRICE_TYPE_CHOICES = [
        ("fixed", "Fixed Price"),
        ("negotiable", "Negotiable"),
        ("price_on_request", "Price on Request"),
    ]

    FURNISHING_CHOICES = [
        ("furnished", "Furnished"),
        ("semi_furnished", "Semi Furnished"),
        ("unfurnished", "Unfurnished"),
        ("not_applicable", "Not Applicable"),
    ]

    FACING_CHOICES = [
        ("north", "North"),
        ("south", "South"),
        ("east", "East"),
        ("west", "West"),
        ("north_east", "North East"),
        ("north_west", "North West"),
        ("south_east", "South East"),
        ("south_west", "South West"),
        ("not_applicable", "Not Applicable"),
    ]

    # Basic Information
    property_id = models.CharField(
        max_length=50,
        unique=True,
        blank=True
    )

    title = models.CharField(max_length=255)

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True
    )

    property_type = models.ForeignKey(
        PropertyType,
        on_delete=models.PROTECT,
        related_name="properties"
    )

    description = models.TextField()

    # Price
    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )

    price_type = models.CharField(
        max_length=30,
        choices=PRICE_TYPE_CHOICES,
        default="fixed"
    )

    # Location
    location = models.CharField(max_length=255)

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    pincode = models.CharField(
        max_length=10,
        blank=True
    )

    address = models.TextField()

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    # Area
    area_sqft = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    plot_area = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    built_up_area = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Property Details
    bedrooms = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    bathrooms = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    floors = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    parking = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    facing = models.CharField(
        max_length=30,
        choices=FACING_CHOICES,
        blank=True
    )

    furnishing = models.CharField(
        max_length=30,
        choices=FURNISHING_CHOICES,
        blank=True
    )

    # Amenities
    amenities = models.ManyToManyField(
        Amenity,
        blank=True,
        related_name="properties"
    )

    # Status
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="available"
    )

    featured = models.BooleanField(default=False)

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["city"]),
            models.Index(fields=["status"]),
            models.Index(fields=["featured"]),
            models.Index(fields=["property_type"]),
            models.Index(fields=["price"]),
        ]

    def save(self, *args, **kwargs):

        if not self.property_id:
            last_property = Property.objects.order_by("-id").first()

            if last_property:
                next_id = last_property.id + 1
            else:
                next_id = 1

            self.property_id = f"PROP-{next_id:05d}"

        if not self.slug:
            self.slug = slugify(self.title)

            original_slug = self.slug
            counter = 1

            while Property.objects.filter(
                slug=self.slug
            ).exclude(pk=self.pk).exists():

                self.slug = f"{original_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.property_id} - {self.title}"


class PropertyImage(models.Model):

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="properties/images/"
    )

    title = models.CharField(
        max_length=255,
        blank=True
    )

    is_primary = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-is_primary", "id"]

    def __str__(self):
        return f"{self.property.title} - Image"


class PropertyVideo(models.Model):

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="videos"
    )

    video = models.FileField(
        upload_to="properties/videos/",
        blank=True,
        null=True
    )

    video_url = models.URLField(
        blank=True
    )

    title = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.property.title} - Video"


class Venture(models.Model):

    name = models.CharField(max_length=255)

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    total_area = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )

    total_plots = models.PositiveIntegerField(
        default=0
    )

    available_plots = models.PositiveIntegerField(
        default=0
    )

    sold_plots = models.PositiveIntegerField(
        default=0
    )

    location = models.CharField(
        max_length=255
    )

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class VenturePlot(models.Model):

    STATUS_CHOICES = [
        ("available", "Available"),
        ("booked", "Booked"),
        ("sold", "Sold"),
    ]

    venture = models.ForeignKey(
        Venture,
        on_delete=models.CASCADE,
        related_name="plots"
    )

    plot_number = models.CharField(
        max_length=50
    )

    area = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    facing = models.CharField(
        max_length=30,
        blank=True
    )

    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="available"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["plot_number"]
        unique_together = ["venture", "plot_number"]

    def __str__(self):
        return f"{self.venture.name} - Plot {self.plot_number}"


from django.db import models


class VisitorEmail(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email