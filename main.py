from commandLine import CLI

def main():
    """
    Main function to initialize and run the CLI tool.
    """
    # You can pass your Google Books API key here if you have one.
    # It's not strictly necessary for basic public searches, but good practice for higher limits.
    # For example: cli_tool = CLI(api_key="YOUR_API_KEY")
    cli_tool = CLI()
    cli_tool.run()

if __name__ == "__main__":
    main()