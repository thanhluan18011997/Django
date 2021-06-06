from learndjango.models import Device


class Demo1:
    def __init__(self, get_response):
        if Device.objects.all().count() == 0:
            Device.objects.bulk_create([Device(name="Linux", count=0),
                                        Device(name="iPhone", count=0),
                                        Device(name="iPad", count=0)])
        self.get_response = get_response

    def __call__(self, request):
        print("All devive visited....")
        response = self.get_response(request)
        return response

    def process_view(self, request, *args, **kwargs):
        """
        trace device visit server
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        list_device = Device.objects.all()
        for device in list_device:
            if device.name in request.META["HTTP_USER_AGENT"]:
                device.count += 1
                device.save()
        for device in list_device:
            print(f"Device: {device.name} =>>>>>>>>>>>{device.count} times")
