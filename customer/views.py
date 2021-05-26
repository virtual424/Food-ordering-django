from django.shortcuts import render,redirect
from django.views import View
from django.db.models import Q
from .models import MenuItem, Category, OrderModel
from django.core.mail import send_mail

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        starter = MenuItem.objects.filter(category__name__contains='Starter')
        Indian_Delicacies = MenuItem.objects.filter(category__name__contains='Indian Delicacies')
        Roti_naan = MenuItem.objects.filter(category__name__contains='Roti And Naan')
        South_Indian = MenuItem.objects.filter(category__name__contains='South Indian')
        Rice = MenuItem.objects.filter(category__name__contains='Rice')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Beverage')

        # pass into context
        context = {
            'starter': starter,
            'Indian_Delicacies': Indian_Delicacies,
            'Roti_naan': Roti_naan,
            'South_Indian': South_Indian,
            'Rice': Rice,
            'desserts': desserts,
            'drinks': drinks,
        }

        # render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))#pk=primary key
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)


            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(price=price,name=name,email=email,street=street,city=city,state=state,zip_code=zip_code)
        order.items.add(*item_ids)

        # after confirmation send mail #
        body = ('thank you for your order, your food will be delivered soon! \n'
                f'your total: {price}')

        send_mail('Thank you for your Order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
            )

        context = {
            'items': order_items['items'],
            'price': price

        }
        return redirect('order-confirmation',pk=order.pk)
       

class OrderConfirmation(View):
    def get(self,request,pk,*args,**kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
        'pk': order.pk,
        'items': order.items,
        'price': order.price
        }

        return render(request, 'customer/order_confirmation.html', context)

    def post(self,request,pk, *args, **kwargs):
        print(request.body)
        return redirect('payment-confirmation')

        

class OrderPayConfirmation(View):
    def get (self,request,*args,**kwargs):
        return render(request,'customer/order_pay_confirmation.html')




class COD(View):
    def get (self,request,*args,**kwargs):
        return render(request,'customer/COD.html')


class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)

class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) | Q(price__icontains=query) | Q(description__icontains=query)
        )

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)
