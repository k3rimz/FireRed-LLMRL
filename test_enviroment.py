#!/usr/bin/env python3
"""Test script to verify environment setup."""

def test_imports():
    """Test all required package imports."""
    packages = {
        'PyTorch': 'torch',
        'OpenCV': 'cv2',
        'NumPy': 'numpy',
        'PIL': 'PIL',
        'Transformers': 'transformers',
        'Ultralytics': 'ultralytics',
        'CLIP': 'open_clip',
        'MSS': 'mss',
        'PyWin32': 'win32gui',
        'PyAutoGUI': 'pyautogui',
        'Matplotlib': 'matplotlib'
    }
    
    failed = []
    for name, package in packages.items():
        try:
            __import__(package)
            print(f"✓ {name} successfully imported")
        except ImportError as e:
            failed.append(name)
            print(f"✗ {name} import failed: {str(e)}")
    
    return failed

def test_cuda():
    """Test CUDA availability."""
    import torch
    cuda_available = torch.cuda.is_available()
    print(f"\nCUDA Available: {'✓' if cuda_available else '✗'}")
    if cuda_available:
        print(f"CUDA Device: {torch.cuda.get_device_name(0)}")
    return cuda_available

def main():
    print("Testing environment setup...\n")
    
    # Test imports
    failed_imports = test_imports()
    
    # Test CUDA
    cuda_available = test_cuda()
    
    # Print summary
    print("\nEnvironment Test Summary:")
    print("------------------------")
    if not failed_imports:
        print("✓ All required packages installed")
    else:
        print(f"✗ Missing packages: {', '.join(failed_imports)}")
    
    print(f"CUDA Status: {'✓ Available' if cuda_available else '✗ Not Available'}")
    
if __name__ == "__main__":
    main()