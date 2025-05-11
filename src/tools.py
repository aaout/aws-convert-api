tools = [
    {
        "toolSpec": {
            "name": "cosine",
            "description": "Calculate the cosine of x.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "x": {
                            "type": "number",
                            "description": "The number to pass to the function.",
                        }
                    },
                    "required": ["x"],
                }
            },
        }
    },
    {
        "toolSpec": {
            "name": "sine",
            "description": "Calculate the sine of x.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "x": {
                            "type": "number",
                            "description": "The number to pass to the function.",
                        }
                    },
                    "required": ["x"],
                }
            },
        }
    },
    {
        "toolSpec": {
            "name": "tangent",
            "description": "Calculate the tangent of x.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "x": {
                            "type": "number",
                            "description": "The number to pass to the function.",
                        }
                    },
                    "required": ["x"],
                }
            },
        }
    },
    {
        "toolSpec": {
            "name": "divide_numbers",
            "description": "Divide x by y.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "x": {"type": "number", "description": "The numerator."},
                        "y": {"type": "number", "description": "The denominator."},
                    },
                    "required": ["x", "y"],
                }
            },
        }
    },
]
