"""
Automatic Ollama installation and setup.

This module handles automatic installation of Ollama and AI models
so users don't need to manually install anything.
"""

import logging
import subprocess
import sys
import platform
import requests
import time
import tempfile
from pathlib import Path
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class OllamaInstaller:
    """Automatically install and configure Ollama."""
    
    def __init__(self):
        """Initialize Ollama installer."""
        self.ollama_url = "http://localhost:11434"
        self.system = platform.system().lower()
        
    def is_ollama_installed(self) -> bool:
        """Check if Ollama is already installed and running.
        
        Returns:
            True if Ollama is accessible
        """
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def is_ollama_process_running(self) -> bool:
        """Check if Ollama process is running (but maybe not responding yet).
        
        Returns:
            True if Ollama process is found
        """
        try:
            if self.system == "windows":
                result = subprocess.run(
                    ["tasklist", "/FI", "IMAGENAME eq ollama.exe"],
                    capture_output=True,
                    text=True
                )
                return "ollama.exe" in result.stdout.lower()
            else:
                result = subprocess.run(
                    ["pgrep", "-f", "ollama"],
                    capture_output=True,
                    text=True
                )
                return result.returncode == 0
        except:
            return False
    
    def install_ollama(self) -> bool:
        """Install Ollama automatically based on OS.
        
        Returns:
            True if installation successful
        """
        logger.info("🔧 Installing Ollama automatically...")
        
        try:
            if self.system == "windows":
                return self._install_windows()
            elif self.system == "darwin":  # macOS
                return self._install_macos()
            elif self.system == "linux":
                return self._install_linux()
            else:
                logger.error(f"Unsupported OS: {self.system}")
                return False
        except Exception as e:
            logger.error(f"Installation failed: {e}")
            return False
    
    def _install_windows(self) -> bool:
        """Install Ollama on Windows.
        
        Returns:
            True if successful
        """
        logger.info("📥 Downloading Ollama for Windows...")
        
        # Download Ollama installer
        installer_url = "https://ollama.com/download/OllamaSetup.exe"
        
        try:
            # Create temp directory
            temp_dir = Path(tempfile.gettempdir()) / "gravity_ollama"
            temp_dir.mkdir(exist_ok=True)
            installer_path = temp_dir / "OllamaSetup.exe"
            
            # Download installer
            logger.info(f"Downloading from {installer_url}...")
            response = requests.get(installer_url, stream=True, timeout=300)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(installer_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            logger.info(f"Progress: {percent:.1f}%")
            
            logger.info("✓ Download complete")
            
            # Run installer silently
            logger.info("🚀 Installing Ollama...")
            result = subprocess.run(
                [str(installer_path), "/SILENT"],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                logger.info("✓ Ollama installed successfully")
                return True
            else:
                logger.error(f"Installation failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Windows installation error: {e}")
            return False
    
    def _install_macos(self) -> bool:
        """Install Ollama on macOS.
        
        Returns:
            True if successful
        """
        logger.info("📥 Installing Ollama on macOS...")
        
        try:
            # Check if Homebrew is available
            result = subprocess.run(
                ["which", "brew"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Install via Homebrew
                logger.info("Using Homebrew to install Ollama...")
                result = subprocess.run(
                    ["brew", "install", "ollama"],
                    capture_output=True,
                    text=True,
                    timeout=600
                )
                
                if result.returncode == 0:
                    logger.info("✓ Ollama installed via Homebrew")
                    return True
            
            # Fallback: Download and install .app
            logger.info("Downloading Ollama.app...")
            installer_url = "https://ollama.com/download/Ollama-darwin.zip"
            
            temp_dir = Path(tempfile.gettempdir()) / "gravity_ollama"
            temp_dir.mkdir(exist_ok=True)
            zip_path = temp_dir / "Ollama.zip"
            
            response = requests.get(installer_url, stream=True, timeout=300)
            response.raise_for_status()
            
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # Unzip and move to Applications
            subprocess.run(["unzip", "-o", str(zip_path), "-d", str(temp_dir)])
            subprocess.run(["mv", str(temp_dir / "Ollama.app"), "/Applications/"])
            
            logger.info("✓ Ollama installed to /Applications/")
            return True
            
        except Exception as e:
            logger.error(f"macOS installation error: {e}")
            return False
    
    def _install_linux(self) -> bool:
        """Install Ollama on Linux.
        
        Returns:
            True if successful
        """
        logger.info("📥 Installing Ollama on Linux...")
        
        try:
            # Use official install script
            install_script = "curl -fsSL https://ollama.com/install.sh | sh"
            
            result = subprocess.run(
                install_script,
                shell=True,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode == 0:
                logger.info("✓ Ollama installed successfully")
                return True
            else:
                logger.error(f"Installation failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Linux installation error: {e}")
            return False
    
    def start_ollama(self) -> bool:
        """Start Ollama service.
        
        Returns:
            True if started successfully
        """
        logger.info("🚀 Starting Ollama service...")
        
        try:
            if self.system == "windows":
                # On Windows, Ollama starts automatically after install
                # Just check if it's running
                time.sleep(3)
                if self.is_ollama_installed():
                    logger.info("✓ Ollama is running")
                    return True
                    
                # Try to start it manually
                subprocess.Popen(
                    ["ollama", "serve"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            else:
                # macOS/Linux
                subprocess.Popen(
                    ["ollama", "serve"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            
            # Wait for Ollama to be ready
            for i in range(30):
                time.sleep(1)
                if self.is_ollama_installed():
                    logger.info("✓ Ollama started successfully")
                    return True
                logger.debug(f"Waiting for Ollama to start... ({i+1}/30)")
            
            logger.warning("Ollama started but not responding yet")
            return False
            
        except Exception as e:
            logger.error(f"Failed to start Ollama: {e}")
            return False
    
    def download_model(self, model_name: str = "llama3.2:3b") -> bool:
        """Download and install an AI model.
        
        Args:
            model_name: Model to download (default: llama3.2:3b - 2GB)
            
        Returns:
            True if download successful
        """
        logger.info(f"📥 Downloading AI model: {model_name}...")
        logger.info("⏳ This may take a few minutes (first time only)...")
        
        try:
            # Check if model already exists
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                for model in models:
                    if model_name in model.get('name', ''):
                        logger.info(f"✓ Model {model_name} already downloaded")
                        return True
            
            # Pull model
            result = subprocess.run(
                ["ollama", "pull", model_name],
                capture_output=True,
                text=True,
                timeout=1800  # 30 minutes max
            )
            
            if result.returncode == 0:
                logger.info(f"✓ Model {model_name} downloaded successfully")
                return True
            else:
                logger.error(f"Model download failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("Model download timed out (slow internet?)")
            return False
        except Exception as e:
            logger.error(f"Model download error: {e}")
            return False
    
    def setup_ollama(self, model_name: str = "llama3.2:3b") -> Tuple[bool, str]:
        """Complete Ollama setup (install + start + download model).
        
        Args:
            model_name: AI model to install
            
        Returns:
            Tuple of (success, message)
        """
        logger.info("🤖 Setting up FREE AI (Ollama)...")
        
        # Step 1: Check if already installed and running
        if self.is_ollama_installed():
            logger.info("✓ Ollama is already running")
            
            # Just ensure model is downloaded
            if self.download_model(model_name):
                return True, f"AI ready with model: {model_name}"
            else:
                return False, "Failed to download AI model"
        
        # Step 2: Check if Ollama is installed but not running
        if self.is_ollama_process_running():
            logger.info("Ollama installed but not responding, restarting...")
            if self.start_ollama():
                if self.download_model(model_name):
                    return True, f"AI ready with model: {model_name}"
        
        # Step 3: Install Ollama
        logger.info("Ollama not found. Installing automatically...")
        logger.info("⏳ This is a one-time setup (takes 2-5 minutes)...")
        
        if not self.install_ollama():
            return False, "Failed to install Ollama. Please install manually: https://ollama.com/download"
        
        # Step 4: Start Ollama
        if not self.start_ollama():
            return False, "Ollama installed but failed to start. Try running: ollama serve"
        
        # Step 5: Download model
        if not self.download_model(model_name):
            return False, f"Ollama running but failed to download model: {model_name}"
        
        logger.info("🎉 AI setup complete!")
        return True, f"AI ready with model: {model_name}"


def ensure_ollama(model_name: str = "llama3.2:3b") -> bool:
    """Ensure Ollama is installed and ready.
    
    This is a convenience function that handles the entire setup process.
    
    Args:
        model_name: AI model to use
        
    Returns:
        True if Ollama is ready to use
    """
    installer = OllamaInstaller()
    success, message = installer.setup_ollama(model_name)
    
    if success:
        logger.info(f"✓ {message}")
    else:
        logger.error(f"✗ {message}")
    
    return success
