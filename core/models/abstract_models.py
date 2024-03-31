from django.db import models

from .models import JsonLD, MetaTags, OpenGraph, SEOContent, TwitterCard


class WithJsonLD(models.Model):
    """
    A base abstract model that provides functionality for generating and saving JSON-LD data.

    Attributes:
        json_ld (OneToOneField): A one-to-one relationship field to the JSON_LD model.
    """

    json_ld = models.OneToOneField(
        JsonLD, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to generate and save JSON-LD data.

        If the json_ld attribute is not set, it generates JSON-LD data using the generate_json_ld function
        and creates a new JSON_LD object with the generated data. Otherwise, it updates the existing JSON_LD
        object with the new data.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

        if not self.json_ld:
            self.json_ld = JsonLD.objects.create()
            self.json_ld.generate()

        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class WithMetaTags(models.Model):
    """
    A base abstract model that provides functionality for managing meta tags.

    This class should be inherited by other models that require meta tags.
    """

    meta_tags = models.OneToOneField(
        MetaTags, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to handle the creation and updating of meta tags.

        If the `meta_tags` field is not set, it creates a new `MetaTags` object
        and associates it with the current instance. Otherwise, it updates the
        existing `MetaTags` object with new data.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """

        if not self.meta_tags:
            self.meta_tags = MetaTags.objects.create()
            self.meta_tags.generate()

        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class WithOpenGraph(models.Model):
    """
    A base model class that provides functionality for generating and retrieving Open Graph data.

    This class should be used as a base class for models that require Open Graph integration.

    Attributes:
        open_graph (OneToOneField): A one-to-one relationship field to the OpenGraph model.

    Methods:
        save(*args, **kwargs): Overrides the save method to generate and save Open Graph data.
        get_open_graph(): Retrieves the Open Graph data as HTML meta tags.

    Meta:
        abstract = True
    """

    open_graph = models.OneToOneField(
        OpenGraph, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to generate and save Open Graph data.

        If the model instance does not have an associated Open Graph object, it generates the data
        using the generate_open_graph function and creates a new OpenGraph object with the data.
        If the model instance already has an associated Open Graph object, it updates the data in
        the existing object.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """

        if not self.open_graph:
            self.open_graph = OpenGraph.objects.create()
            self.open_graph.generate()

        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class WithTwitterCard(models.Model):
    """
    A mixin class that provides functionality for generating and managing Twitter cards.

    Attributes:
        twitter_card (TwitterCard): A one-to-one relationship field to the TwitterCard model.

    Methods:
        save(*args, **kwargs): Overrides the save method to generate and save a Twitter card if it doesn't exist, or update an existing one.
        get_twitter_card(): Returns the HTML meta tags for the Twitter card data.
    """

    twitter_card = models.OneToOneField(
        TwitterCard, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to generate and save a Twitter card if it doesn't exist, or update an existing one.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

        if not self.twitter_card:
            self.twitter_card = TwitterCard.objects.create()
            self.twitter_card.generate()

        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class WithSEOContent(models.Model):
    """
    A base model class that provides SEO content functionality.

    This class is intended to be inherited by other models that require SEO content.
    It provides methods for generating and retrieving SEO content.

    Attributes:
        seo_content (SEOContent): The SEO content associated with the model.

    Methods:
        save(*args, **kwargs): Overrides the default save method to handle SEO content creation and updates.
        get_seo_content(): Retrieves the SEO content data associated with the model.
    """

    seo_content = models.OneToOneField(
        SEOContent, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to handle SEO content creation and updates.

        If the model does not have an associated SEO content, it generates the content
        using the generate_seo_content function and creates a new SEOContent object.
        If the model already has an associated SEO content, it updates the content.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

        if not self.seo_content:
            self.seo_content = SEOContent.objects.create()
            self.seo_content.generate()

        super().save(*args, **kwargs)

    class Meta:
        abstract = True
