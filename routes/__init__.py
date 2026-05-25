def register_blueprints(app):
    from routes.health import health_bp
    from routes.employee import employee_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(employee_bp)
