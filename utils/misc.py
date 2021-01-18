def external_id_to_res_model_data(env, external_id):
    module, name = external_id.split('.')
    resource = env['ir.model.data'].search([
        ('module', '=', module),
        ('name', '=', name)
    ])
    return resource
# end


def external_id_to_id(env, external_id):
    resource = external_id_to_res_model_data(env, external_id)
    return resource.res_id
# end


def external_id_to_obj(env, external_id):
    resource = external_id_to_res_model_data(env, external_id)
    record = env[resource.model].browse(resource.id)
    return record
# end
