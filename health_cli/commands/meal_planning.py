import typer
from health_cli.db.database import get_session
from health_cli.models.meal_plan_entry import MealPlan
from health_cli.models.meal_plan_entry import create_meal_plan, update_meal_plan, list_meal_plans

meal_app = typer.Typer()

# --- CLI commands using high-level helper functions ---
@meal_app.command("add")
def add_meal_plan(user: str, week: int, meals: str):
    """
    Add a meal plan for a user (meals as a comma-separated string, e.g., 'Oatmeal,Lunch Salad,Dinner Stir Fry').
    """
    session = get_session()
    try:
        plan = create_meal_plan(session, user, week, meals)
        typer.echo(f"✅ Meal plan added for {user} (Week {week}): {plan.meals}")
    except ValueError as e:
        typer.echo(f"❌ Error: {e}")
    finally:
        session.close()

@meal_app.command("update")
def update_plan(plan_id: int, week: int = None, meals: str = None):
    """Update a meal plan by ID."""
    session = get_session()
    try:
        updated = update_meal_plan(session, plan_id, week, meals)
        typer.echo(f"✅ Meal Plan #{updated.id} updated.")
    except ValueError as e:
        typer.echo(f"❌ Error: {e}")
    finally:
        session.close()

@meal_app.command("list")
def list_meals(user: str):
    """List all meal plans for a user."""
    session = get_session()
    try:
        plans = list_meal_plans(session, user)
        if not plans:
            typer.echo(f"⚠️ No meal plans found for {user}")
        for plan in plans:
            typer.echo(f"[ID {plan.id}] Week {plan.week_number} → Meals: {plan.meals}")
    except ValueError as e:
        typer.echo(f"❌ Error: {e}")
    finally:
        session.close()

# --- Additional direct DB operations for day-by-day meal tracking ---
@meal_app.command("add-daily")
def add_daily_meal(user_id: int, day: str, meal: str):
    """Add a single meal entry for a specific day."""
    db = get_session()
    meal_plan = MealPlan(user_id=user_id, day=day, meal=meal)
    db.add(meal_plan)
    db.commit()
    db.refresh(meal_plan)
    db.close()
    typer.echo(f"✅ Meal plan added: {day} - {meal}")

@meal_app.command("update-daily")
def update_daily_meal(meal_plan_id: int, day: str = None, meal: str = None):
    """Update a daily meal plan entry."""
    db = get_session()
    plan = db.query(MealPlan).filter(MealPlan.id == meal_plan_id).first()
    if not plan:
        typer.echo("❌ Meal plan not found.")
    else:
        if day:
            plan.day = day
        if meal:
            plan.meal = meal
        db.commit()
        typer.echo("✅ Meal plan updated.")
    db.close()

@meal_app.command("delete")
def delete_meal(meal_plan_id: int):
    """Delete a meal plan entry by ID."""
    db = get_session()
    plan = db.query(MealPlan).filter(MealPlan.id == meal_plan_id).first()
    if not plan:
        typer.echo("❌ Meal plan not found.")
    else:
        db.delete(plan)
        db.commit()
        typer.echo("🗑 Meal plan deleted.")
    db.close()
