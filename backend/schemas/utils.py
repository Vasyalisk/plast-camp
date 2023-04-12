def init_schemas():
    """
    Update forward references on Pydantic models to allow circular imports
    :return:
    """
    import schemas.camps
    import schemas.users

    schemas.camps.MembershipItemResponse.update_forward_refs(UserResponse=schemas.users.DetailResponse)
    schemas.users.MembershipItemResponse.update_forward_refs(CampResponse=schemas.camps.DetailResponse)
