import typer
from health_cli.db.database import get_session
from health_cli.models.mealplan_entry import create_meal_plan, update_meal_plan, list_meal_plans

meal_app = typer.Typer()

@meal_app.command("add")
def add_meal_plan(user: str, week: int, meals: str):
    """
    Add a meal plan for a user (meals as a string, e.g., 'Oatmeal,Lunch Salad,Dinner Stir Fry').
    """
    session = get_session()
    try:
        plan = create_meal_plan(session, user, week, meals)
        typer.echo(f"Meal plan added for {user} (Week {week}): {plan.meals}")
    except ValueError as e:
        typer.echo(f"Error: {e}")
    finally:
        session.close()

@meal_app.command("update")
def update_plan(plan_id: int, week: int = None, meals: str = None):
    """Update a meal plan by ID."""
    session = get_session()
    try:
        updated = update_meal_plan(session, plan_id, week, meals)
        typer.echo(f"Meal Plan #{updated.id} updated.")
    except ValueError as e:
        typer.echo(f"Error: {e}")
    finally:
        session.close()

@meal_app.command("list")
def list_meals(user: str):
    """List all meal plans for a user."""
    session = get_session()
    try:
        plans = list_meal_plans(session, user)
        if not plans:
            typer.echo(f"No meal plans found for {user}")
        for plan in plans:
            typer.echo(f"[ID {plan.id}] Week {plan.week_number} → Meals: {plan.meals}")
    except ValueError as e:
        typer.echo(f"Error: {e}")
    finally:
        session.close()
