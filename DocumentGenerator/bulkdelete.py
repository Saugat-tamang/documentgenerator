from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse

# START REAL TIME VALIDATION DJANGO CODE FROM HERE
def check_field_exists(request, model, field_name, user_filter=None, exclude_id_param='id', client_id=None, client_field=None):
    if request.method != 'GET':
        return JsonResponse({'exists': False}, status=400)

    value                           = request.GET.get(field_name, '').strip()
    exclude_id                      = request.GET.get(exclude_id_param, None)

    # Use session client_id only if not passed
    if client_id is None:
        client_id = request.session.get('client_id')

    if not value:
        return JsonResponse({'exists': False})

    qs                              = model.objects.all()

    # Apply user filter if provided
    if user_filter:
        filter_cond                 = user_filter(request.user)
        qs                          = qs.filter(**filter_cond) if isinstance(filter_cond, dict) else qs.filter(filter_cond)

    # Filter by client_field if provided and exists
    if client_field and client_id:
        try:
            client_id_int           = int(client_id)
            if client_field in [f.name for f in model._meta.fields]:
                qs                  = qs.filter(**{f"{client_field}_id": client_id_int})
        except (ValueError, TypeError):
            pass

    # Filter by the main field value
    filter_kwargs                   = {f"{field_name}__iexact": value}
    qs                              = qs.filter(**filter_kwargs)

    # Exclude a specific ID if provided
    if exclude_id and exclude_id.isdigit():
        qs                          = qs.exclude(id=int(exclude_id))

    return JsonResponse({'exists': qs.exists()})


def datatable_json_response(request, model, columns, filter_kwargs=None, search_fields=None, extra_context=None):
    try:
        if filter_kwargs is None:
            filter_kwargs           = {}

        if search_fields is None:
            search_fields           = []

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            search_value            = request.GET.get('search[value]', '').strip()
            start                   = int(request.GET.get('start', 0))
            length                  = int(request.GET.get('length', 10))
            draw                    = int(request.GET.get('draw', 1))

            qs = model.objects.filter(**filter_kwargs)

            if search_value:
                queries             = Q()
                for field in search_fields:
                    queries |= Q(**{f"{field}__icontains": search_value})
                qs                  = qs.filter(queries)

            total_records           = qs.count()

            values_qs = qs.values(*columns)[start:start + length]

            data                    = list(values_qs)
            for i, item in enumerate(data, start=start + 1):
                item['sn'] = i
                
                for key, value in item.items():
                    if value is None or value == "":
                        item[key] = "-"

            response = {
                'draw'              : draw,
                'recordsTotal'      : total_records,
                'recordsFiltered'   : total_records,
                'data'              : data,
            }
            return JsonResponse(response)

        if extra_context:
            return render(request, extra_context.get('template_name'), extra_context)

        return JsonResponse({'error': 'Invalid request'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)