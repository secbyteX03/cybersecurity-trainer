"""
Test script for Cybersecurity Command Trainer
"""
import sys
import io
from unittest.mock import patch
from trainer import CyberSecTrainer

def test_menu_display():
    """Test that the main menu displays correctly"""
    trainer = CyberSecTrainer()
    
    # Redirect stdout to capture the output
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    try:
        # Test banner display
        trainer.show_banner()
        output = sys.stdout.getvalue()
        assert "CYBERSECURITY COMMAND TRAINER" in output
        
        # Test menu display
        trainer.show_main_menu()
        output = sys.stdout.getvalue()
        assert "MAIN MENU" in output
        assert "Linux Basics" in output
        assert "Networking" in output
        
        print("[PASS] Menu display test passed!")
        return True
    except AssertionError as e:
        print(f"[FAIL] Menu display test failed: {e}")
        return False
    finally:
        sys.stdout = old_stdout

def test_help_screen():
    """Test that the help screen displays correctly"""
    trainer = CyberSecTrainer()
    
    # Redirect stdout to capture the output
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    try:
        trainer.show_help()
        output = sys.stdout.getvalue()
        assert "HOW TO USE THIS TRAINER" in output
        assert "SAFE learning environment" in output
        
        print("[PASS] Help screen test passed!")
        return True
    except AssertionError as e:
        print(f"[FAIL] Help screen test failed: {e}")
        return False
    finally:
        sys.stdout = old_stdout

if __name__ == "__main__":
    print("\n=== RUNNING TESTS ===\n")
    
    # Run tests
    menu_test = test_menu_display()
    help_test = test_help_screen()
    
    # Print summary
    print("\n=== TEST SUMMARY ===")
    print(f"Menu Display: {'PASS' if menu_test else 'FAIL'}")
    print(f"Help Screen:  {'PASS' if help_test else 'FAIL'}")
    
    if menu_test and help_test:
        print("\nAll tests passed! The trainer's core functionality appears to be working.")
        print("You can now run 'python trainer.py' to use the interactive trainer.")
    else:
        print("\nSome tests failed. Please check the error messages above.")
