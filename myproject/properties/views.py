from django.shortcuts import get_object_or_404
from .forms import PropertyForm

# 1. Admin Property List View (Dashboard se click karne par saari properties dikhengi)
def admin_property_list(request):
    properties = Property.objects.all().order_by('-id')
    return render(request, 'admin/property_list.html', {'properties': properties})

# 2. Add Property View
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Property added successfully!")
            return redirect('admin_property_list')
    else:
        form = PropertyForm()
    return render(request, 'admin/add_property.html', {'form': form})

# 3. Edit Property View
def edit_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Property updated successfully!")
            return redirect('admin_property_list')
    else:
        form = PropertyForm(instance=property_obj)
    return render(request, 'admin/edit_property.html', {'form': form, 'property': property_obj})

# 4. Delete Property View
def delete_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    property_obj.delete()
    messages.success(request, "Property deleted successfully!")
    return redirect('admin_property_list')