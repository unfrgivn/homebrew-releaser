# typed: true
# frozen_string_literal: true

# This file was generated by Homebrew Releaser. DO NOT EDIT.
class TestGenerateFormulaDarwinMatrix < Formula
  

  desc "Release scripts, binaries, and executables to github"
  homepage "https://github.com/Justintime50/test-generate-formula-darwin-matrix"
  url "https://github.com/Justintime50/test-generate-formula-darwin-matrix/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"
  license "MIT"

  on_macos do
    on_intel do
      url "https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-darwin-amd64.tar.gz"
      sha256 "0000000000000000000000000000000000000000000000000000000000000000"
    end

    on_arm do
      url "https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-darwin-arm64.tar.gz"
      sha256 "0000000000000000000000000000000000000000000000000000000000000000"
    end
  end

  def install
    bin.install "src/secure-browser-kiosk.sh" => "secure-browser-kiosk"
  end
end
