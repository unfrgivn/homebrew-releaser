import re
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

import chevron  # type: ignore
import woodchips

from homebrew_releaser.constants import (
    LOGGER_NAME,
    TARGET_DARWIN_AMD64,
    TARGET_DARWIN_ARM64,
    TARGET_LINUX_AMD64,
    TARGET_LINUX_ARM64,
)


class Formula:
    @staticmethod
    def generate_formula_data(
        owner: str,
        repo_name: str,
        repository: Dict[str, Any],
        checksums: List[Dict[str, str]],
        install: str,
        tar_url: str,
        depends_on: Optional[str] = None,
        test: Optional[str] = None,
        download_strategy: Optional[str] = None,
        custom_require: Optional[str] = None,
        formula_includes: Optional[str] = None,
        version: Optional[str] = None,
    ) -> str:
        """Generates the formula data for Homebrew.

        We attempt to ensure generated formula will pass `brew audit --strict --online` if given correct inputs:
        - Proper class name
        - 80 characters or less desc field (alphanumeric characters and does not start with
            an article or the name of the formula)
        - Homepage
        - URL points to the tar file
        - Checksum matches the url archive
        - Proper installable binary
        - Test is included
        - No version attribute if Homebrew can reliably infer the version from the tar URL (GitHub tag)
        - Enable typing
        - Enable frozen_string_literal
        """
        logger = woodchips.get(LOGGER_NAME)

        max_desc_field_length = 80  # `brew audit` wants no more than 80 characters in the desc field

        class_name = re.sub(r'[-_. ]+', '', repo_name.title())
        license_type = repository['license'].get('spdx_id', '') if repository.get('license') else ''
        description = (
            re.sub(r'[.!]+', '', repository.get('description', '')[:max_desc_field_length]).strip().capitalize()
        )

        # If the first word of the desc is an article or the name of the formula, we cut it out per `brew audit`
        articles = {
            'a',
            'an',
            'the',
        }
        if description:
            first_word_of_desc = description.split(' ', 1)
            if first_word_of_desc[0].lower() in articles or first_word_of_desc[0].lower() == class_name.lower():
                description = first_word_of_desc[1].strip().capitalize()
        else:
            description = 'NA'

        dependencies_object: Dict[str, Any] = {
            'dependencies': [],
        }
        dependencies_list = dependencies_object['dependencies']
        if depends_on:
            dependencies = [dependency.strip() for dependency in depends_on.split('\n') if dependency]

            # `brew audit` wants dependencies sorted
            for dependency in sorted(dependencies):
                dependencies_list.append({'dependency': dependency})

        darwin_amd64_url = None
        darwin_amd64_checksum = None
        darwin_arm64_url = None
        darwin_arm64_checksum = None
        linux_amd64_url = None
        linux_amd64_checksum = None
        linux_arm64_url = None
        linux_arm64_checksum = None
        for index, checksum in enumerate(checksums):
            checksum_filename = next(iter(checksum))
            checksum_url = checksum[checksum_filename]['url']  # type: ignore

            # Autogenerated tar URL is the first one
            if index == 0:
                autogenerated_tar_checksum = checksum[checksum_filename]['checksum']  # type: ignore

            if checksum_url.endswith('darwin-amd64.tar.gz') and TARGET_DARWIN_AMD64:
                darwin_amd64_url = checksum_url
                darwin_amd64_checksum = checksum[checksum_filename]['checksum']  # type: ignore
            elif checksum_url.endswith('darwin-arm64.tar.gz') and TARGET_DARWIN_ARM64:
                darwin_arm64_url = checksum_url
                darwin_arm64_checksum = checksum[checksum_filename]['checksum']  # type: ignore
            elif checksum_url.endswith('linux-amd64.tar.gz') and TARGET_LINUX_AMD64:
                linux_amd64_url = checksum_url
                linux_amd64_checksum = checksum[checksum_filename]['checksum']  # type: ignore
            elif checksum_url.endswith('linux-arm64.tar.gz') and TARGET_LINUX_ARM64:
                linux_arm64_url = checksum_url
                linux_arm64_checksum = checksum[checksum_filename]['checksum']  # type: ignore

        # We set these so we can properly space items only if both are present
        darwin_amd_and_arm = darwin_amd64_url and darwin_arm64_url
        linux_amd_and_arm = linux_amd64_url and linux_arm64_url

        # Ruby template data MUST remain double spaced to conform to `brew audit`.
        # You may notice some template checks have a line break after the opening tag, this is to ensure
        # we only add that line break when that section is present.
        template = """# typed: true
# frozen_string_literal: true
{{# custom_require}}

require_relative "{{custom_require}}"
{{/ custom_require}}

# This file was generated by Homebrew Releaser. DO NOT EDIT.
class {{class_name}} < Formula
  {{{formula_includes}}}

  desc "{{description}}"
  homepage "https://github.com/{{owner}}/{{repo_name}}"
  url "{{tar_url}}"{{# download_strategy}}, using: {{download_strategy}}{{/ download_strategy}}
  {{# version}}
  version "{{version}}"
  {{/ version}}
  sha256 "{{autogenerated_tar_checksum}}"
  {{# license_type}}
  license "{{license_type}}"
  {{/ license_type}}

  {{# dependencies}}
  depends_on {{{dependency}}}
  {{/ dependencies}}
  {{# darwin}}

  on_macos do
    {{# darwin_amd64_url}}
    on_intel do
      url "{{darwin_amd64_url}}"{{# download_strategy}}, using: {{download_strategy}}{{/ download_strategy}}
      sha256 "{{darwin_amd64_checksum}}"
    end
    {{/ darwin_amd64_url}}
    {{# darwin_amd_and_arm}}

    {{/ darwin_amd_and_arm}}
    {{# darwin_arm64_url}}
    on_arm do
      url "{{darwin_arm64_url}}"{{# download_strategy}}, using: {{download_strategy}}{{/ download_strategy}}
      sha256 "{{darwin_arm64_checksum}}"
    end
    {{/ darwin_arm64_url}}
  end
  {{/ darwin}}
  {{# linux}}

  on_linux do
    {{# linux_amd64_url}}
    on_intel do
      url "{{linux_amd64_url}}"{{# download_strategy}}, using: {{download_strategy}}{{/ download_strategy}}
      sha256 "{{linux_amd64_checksum}}"
    end
    {{/ linux_amd64_url}}
    {{# linux_amd_and_arm}}

    {{/ linux_amd_and_arm}}
    {{# linux_arm64_url}}
    on_arm do
      url "{{linux_arm64_url}}"{{# download_strategy}}, using: {{download_strategy}}{{/ download_strategy}}
      sha256 "{{linux_arm64_checksum}}"
    end
    {{/ linux_arm64_url}}
  end
  {{/ linux}}

  def install
    {{{install_instructions}}}
  end
  {{# test_instructions}}

  test do
    {{{test_instructions}}}
  end
  {{/ test_instructions}}
end
"""

        target_darwin = True if TARGET_DARWIN_AMD64 or TARGET_DARWIN_ARM64 else False
        target_linux = True if TARGET_LINUX_AMD64 or TARGET_LINUX_ARM64 else False

        template_data = {
            'template': template,
            'data': {
                'class_name': class_name,
                'description': description,
                'owner': owner,
                'repo_name': repo_name,
                'tar_url': tar_url,
                'autogenerated_tar_checksum': autogenerated_tar_checksum,
                'license_type': license_type,
                'dependencies': dependencies_list,
                'install_instructions': install.strip(),
                'test_instructions': test.strip() if test else None,
                'download_strategy': download_strategy,
                'custom_require': custom_require,
                'formula_includes': formula_includes.strip() if formula_includes else None,
                'version': version,
                'darwin_amd64_url': darwin_amd64_url,
                'darwin_amd64_checksum': darwin_amd64_checksum,
                'darwin_arm64_url': darwin_arm64_url,
                'darwin_arm64_checksum': darwin_arm64_checksum,
                'linux_amd64_url': linux_amd64_url,
                'linux_amd64_checksum': linux_amd64_checksum,
                'linux_arm64_url': linux_arm64_url,
                'linux_arm64_checksum': linux_arm64_checksum,
                'darwin_amd_and_arm': darwin_amd_and_arm,
                'linux_amd_and_arm': linux_amd_and_arm,
                'darwin': target_darwin,
                'linux': target_linux,
            },
        }

        # TODO: We replace the multiple newlines here for shortcomings in the chevron template above so that
        # `brew audit` passes correctly.
        rendered_template = (
            chevron.render(**template_data)
            .replace('\n\n\n  def install', '\n\n  def install')
            .replace('\n\n\n  on_macos', '\n\n  on_macos')
            .replace('\n\n\n  on_linux', '\n\n  on_linux')
        )

        logger.info('Homebrew formula generated successfully!')
        logger.debug(rendered_template)

        return rendered_template
