# Getting an API Key for the Virtual Try-On System

This guide will walk you through the process of obtaining an API key for the Segmind Try-On Diffusion API, which is used in our Virtual Try-On System.

## Segmind API Key (Recommended)

1. **Create a Segmind Account**
   - Go to [Segmind Cloud](https://cloud.segmind.com/sign-up)
   - Sign up for a new account using your email or Google account
   - Verify your email if required

2. **Access the API Keys Section**
   - Log in to your Segmind account
   - Navigate to the [API Keys section](https://cloud.segmind.com/console/api-keys)
   - If you can't find it, look for "Console" or "Dashboard" in the main menu

3. **Generate a New API Key**
   - Click on "Create New API Key" or a similar button
   - Give your API key a name (e.g., "Virtual Try-On App")
   - Copy the generated API key immediately (it may only be shown once)

4. **Add Credits to Your Account**
   - Segmind operates on a credit-based system
   - New accounts typically come with some free credits
   - You can purchase additional credits if needed

5. **Add the API Key to Your Application**
   - Create a file named `.env` in the root directory of the project
   - Add the following line to the file:
     ```
     SEGMIND_API_KEY=your_api_key_here
     ```
   - Replace `your_api_key_here` with the actual API key you copied

## Alternative: FASHN API Key

If you prefer to use the FASHN API instead:

1. **Create a FASHN Account**
   - Go to [FASHN.AI](https://app.fashn.ai)
   - Sign up for a new account

2. **Access the API Section**
   - Log in to your FASHN account
   - Navigate to the API section (usually found in account settings or developer tools)

3. **Generate a New API Key**
   - Look for an option to create or generate a new API key
   - Note that FASHN API starts at $10 for usage

4. **Add the API Key to Your Application**
   - Create a file named `.env` in the root directory of the project
   - Add the following line to the file:
     ```
     FASHN_API_KEY=your_fashn_api_key_here
     ```
   - Replace `your_fashn_api_key_here` with the actual API key you received

5. **Modify the Application Code**
   - You'll need to modify the `app.py` file to use the FASHN API instead of Segmind
   - Look for the `call_segmind_api` function and replace it with code for the FASHN API
   - The FASHN API endpoint is typically `https://api.fashn.ai/v1/run`

## Troubleshooting

- **API Key Not Working**: Make sure you've copied the entire key correctly without any extra spaces
- **Out of Credits**: Check your account dashboard to see if you have enough credits
- **API Rate Limiting**: Most APIs have rate limits; check the documentation for details
- **Error Messages**: If you receive specific error messages, consult the API provider's documentation

## API Usage Considerations

- Both APIs charge based on usage (number of API calls or credits)
- Monitor your usage to avoid unexpected charges
- Consider implementing caching if you expect high usage
- Be aware of the data retention policies of the API provider

## Next Steps

Once you have your API key set up, you can run the application and start using the virtual try-on feature. Refer to the main README.md file for instructions on how to run the application.
