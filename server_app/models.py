from django.db import models
import os
from django.conf import settings
import hashlib
from django.dispatch import receiver
from django.db.models.signals import post_save


def hash_directory_path(instance, filename):
	BLOCKSIZE = 65536
	hasher = hashlib.sha1()
	buf = instance.file.read(BLOCKSIZE)
	while len(buf) > 0:
		hasher.update(buf)
		buf = instance.file.read(BLOCKSIZE)
	hash = hasher.hexdigest()
	os.makedirs(os.path.join(getattr(settings, "BASE_DIR"), 'store', str(hash[:2])), exist_ok=True)
	return os.path.join(getattr(settings, "BASE_DIR"), 'store', str(hash[:2]), hash)


class File(models.Model):
	hash = models.CharField(max_length=50, unique=True, null=False, default='')
	file = models.FileField(blank=False, null=False, upload_to=hash_directory_path)

	def __str__(self):
		return os.path.basename(self.hash)

	def set_hash(self, hash):
		self.hash = hash
		self.save()


@receiver([post_save], sender=File)
def update_calculated_fields(sender, instance, **kwargs):
	post_save.disconnect(update_calculated_fields, sender=sender)
	instance.set_hash(os.path.basename(instance.file.name))
	post_save.connect(update_calculated_fields, sender=sender)

