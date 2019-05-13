from allauth.account.adapter import DefaultAccountAdapter


class ExpandAdapterResponse(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        print('got here')
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        print(data.get('name'))
        user.name = data.get('name') if data.get('name') else ''
        user.credit_card = data.get(
            'credit_card') if data.get('credit_card') else ''
        user.address_1 = data.get('address_1') if data.get('address_1') else ''
        user.address_2 = data.get('address_2') if data.get('address_2') else ''
        user.city = data.get('city') if data.get('city') else ''
        user.region = data.get('region') if data.get('region') else ''
        user.postal_code = data.get(
            'postal_code') if data.get('postal_code') else ''
        user.country = data.get('country') if data.get('country') else ''
        user.day_phone = data.get('day_phone') if data.get('day_phone') else ''
        user.eve_phone = data.get('eve_phone') if data.get('eve_phone') else ''
        user.mob_phone = data.get('mob_phone') if data.get('mob_phone') else ''
        user.save()
        return user
