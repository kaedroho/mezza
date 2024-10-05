from mezza.projects.operations import create_project


def create_project_from_idea(idea):
    return create_project(
        title=idea.title,
        description=idea.description,
        space=idea.space,
    )
