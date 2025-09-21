#!/usr/bin/env python3
"""
This application generates QR codes from URL inputs using Python and the qrcode library.
The generated QR codes can be displayed on screen and saved as image files.
"""

import qrcode
import qrcode.constants
from PIL import Image
import os
import sys
from datetime import datetime


class QRCodeGenerator:
    
    def __init__(self):
        """Initialize the QR Code Generator with default settings."""
        self.version = 1
        self.box_size = 10
        self.border = 4
        self.error_correction = qrcode.constants.ERROR_CORRECT_M

    def validate_url(self, url):
        """
        Validates if the input string is a proper URL format.
        
        """
        # Basic URL validation
        if not url or not isinstance(url, str):
            return False
        
        # Check if URL starts with http:// or https://
        if url.startswith(('http://', 'https://')):
            return True

        # Checks basic domain format
        if '.' in url and not url.startswith('.') and not url.endswith('.'):
            return True
            
        return False
    
    def format_url(self, url):
        """
        Formats the URL to ensure it has a proper protocol prefix.
        """
        if not url.startswith(('http://', 'https://')):
            return f"https://{url}"
        return url
    
    def generate_qr_code(self, url, filename=None):
        """
        Generate a QR code for the URL.
        
        """
        try:
            # Validates the URL
            if not self.validate_url(url):
                return False, "Please enter a valid URL.", None
            
            # Format URL
            formatted_url = self.format_url(url)
            
            # Create QR code instance
            qr = qrcode.QRCode(
                version=self.version,
                error_correction=self.error_correction,
                box_size=self.box_size,
                border=self.border,
            )
            
            # Add data to QR code
            qr.add_data(formatted_url)
            qr.make(fit=True)
            
            # Create QR code image with professional styling
            qr_image = qr.make_image(
                fill_color="black", 
                back_color="white"
            )
            
            # Generate filename
            if not filename:
                safe_url = "".join(c for c in url if c.isalnum() or c in ('-', '_'))[:20]
                filename = f"{safe_url}.png"
            
            # Ensure filename has proper extension
            if not filename.lower().endswith('.png'):
                filename += '.png'
            
            # Save the QR code
            output_dir = "qr_codes_output"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            filepath = os.path.join(output_dir, filename)
            qr_image.save(filepath)
            
            return True, f"QR code generated successfully! Saved as: {filepath}", qr_image
            
        except Exception as e:
            return False, f"Error generating QR code: {str(e)}", None
    
    def display_qr_info(self, url, success, message):
        """
        Display information about the QR code generation process.
        """
        print("\n" + "="*60)
        print(f"Input URL: {url}")
        print(f"Status: {'SUCCESS' if success else 'FAILED'}")
        print(f"Message: {message}")
        print("="*60)


def main():
    """
    Main function to run the QR Code Generator application.
    """
    print("Welcome to QR Code Generator!")
    print("This application generates QR codes from URL inputs.")
    print("-" * 50)
    
    # Initialize the QR code generator
    generator = QRCodeGenerator()
    
    while True:
        try:
            # Get URL input from user
            print("\nOptions:")
            print("1. Generate QR code from URL")
            print("2. Exit application")
            
            choice = input("\nEnter your choice (1 or 2): ").strip()
            
            if choice == '2':
                print("Goodbye!")
                break
            elif choice == '1':
                # Get URL from user
                url = input("\nEnter the URL to generate QR code: ").strip()

                # Validate URL
                if not url:
                    print("Error: URL cannot be empty.")
                    continue
                
                print("\nGenerating QR code...")
                
                # Generate QR code
                success, message, qr_image = generator.generate_qr_code(url)
                
                # Display results
                generator.display_qr_info(url, success, message)
                
                if success:
                    # Try to display the image (platform dependent)
                    try:
                        qr_image.show()
                        print("QR code image displayed in your default image viewer.")
                    except Exception as e:
                        print(f"Note: Could not display image automatically: {e}")
                        print("Please check the output folder for your QR code file.")
                
            else:
                print("Invalid choice. Please enter 1 or 2.")

        # Handle keyboard interrupt
        except KeyboardInterrupt:
            print("\n\nApplication interrupted by user.")
            print("Thank you for using the QR Code Generator!")
            sys.exit(0)
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            print("Please try again.")

# Run the application
if __name__ == "__main__":
    main()