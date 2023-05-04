import eggsample


@eggsample.hookimpl
def eggsample_add_ingredients(ingredients):
    """Here the caller expects us to return a list."""
    return (
        ["lovely spam", "wonderous spam"]
        if "egg" in ingredients
        else ["splendiferous spam", "magnificent spam"]
    )


@eggsample.hookimpl
def eggsample_prep_condiments(condiments):
    """Here the caller passes a mutable object, so we mess with it directly."""
    try:
        del condiments["steak sauce"]
    except KeyError:
        pass
    condiments["spam sauce"] = 42
    return "Now this is what I call a condiments tray!"
