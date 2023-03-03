# typed: false
# frozen_string_literal: true

require_relative "../mock_download_strategy"

# This file was generated by Homebrew Releaser. DO NOT EDIT.
class TestGenerateFormulaDownloadStrategy < Formula
  desc "Release scripts, binaries, and executables to github"
  homepage "https://github.com/Justintime50/test-generate-formula-download-strategy"
  url "https://github.com/Justintime50/test-generate-formula-download-strategy/archive/v0.1.0.tar.gz", using: CustomDownloadStrategy
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"
  license "MIT"

  on_macos do
    on_intel do
      url "https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-darwin-amd64.tar.gz", using: CustomDownloadStrategy
      sha256 "0000000000000000000000000000000000000000000000000000000000000000"
    end

    on_arm do
      url "https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-darwin-arm64.tar.gz", using: CustomDownloadStrategy
      sha256 "0000000000000000000000000000000000000000000000000000000000000000"
    end
  end

  on_linux do
    on_intel do
      url "https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-linux-amd64.tar.gz", using: CustomDownloadStrategy
      sha256 "0000000000000000000000000000000000000000000000000000000000000000"
    end

    on_arm do
      url "https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-linux-arm64.tar.gz", using: CustomDownloadStrategy
      sha256 "0000000000000000000000000000000000000000000000000000000000000000"
    end
  end

  def install
    bin.install "src/secure-browser-kiosk.sh" => "secure-browser-kiosk"
  end
end
