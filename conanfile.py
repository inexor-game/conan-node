from conans import ConanFile, ConfigureEnvironment, tools
from conans.tools import download, unzip
import os
import shutil
import textwrap

class NodeConan( ConanFile ):
  name = 'node'
  version = '6.1.0'
  license = 'MIT https://github.com/silkedit/node/blob/silkedit/LICENSE'
  url = 'https://github.com/silkedit/conan-node'
  settings = 'os', 'compiler', 'build_type', 'arch'
  options = { 'shared': [ True, False ] }
  default_options = 'shared=True'
  source_dir = '%s-%s' % ( name, version )
  short_paths=True

  def source( self ):
    zip_name = '%s.tar.gz' % ( self.version )
    download( 'https://github.com/silkedit/node/archive/%s' % zip_name, zip_name )
    unzip( zip_name )
    os.unlink( zip_name )

  def build( self ):
    if self.settings.os == 'Windows':
      flags = 'nosign'
      if self.options.shared:
        flags += ' shared'
      if self.settings.build_type == 'Debug':
        flags += ' debug'
      if self.settings.arch == 'x86':
        flags += ' x86'
      elif self.settings.arch == 'x86_64':
        flags += ' x64'
      build_command = 'cd %s & vcbuild.bat %s' % ( self.source_dir, flags )
      self.output.info( 'build_command: %s' % build_command )
      self.run( build_command )
    else:
      env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
      flags = '--enable-shared' if self.options.shared else ''
      if self.settings.build_type == 'Debug':
        flags += ' --debug'
      configure_command = 'cd %s && %s ./configure %s' % ( self.source_dir, env.command_line, flags )
      self.output.info( 'Configure with: %s' % configure_command )
      self.run( configure_command )
      self.run( 'cd %s && %s make -j2' % ( self.source_dir, env.command_line) )

  def package( self ):
    self.copy( '*.h', dst='include', src='%s/src' % self.source_dir )
    self.copy( '*.h', dst='deps/v8', src='%s/deps/v8' % self.source_dir )
    self.copy( '*.h', dst='deps/v8/include', src='%s/deps/v8/include' % self.source_dir )
    self.copy( '*.h', dst='deps/uv/include', src='%s/deps/uv/include' % self.source_dir )
    self.copy( '*.h', dst='deps/uv/src', src='%s/deps/uv/src' % self.source_dir )
    self.copy( '*.h', dst='deps/cares/include', src='%s/deps/cares/include' % self.source_dir )
    self.copy( '*.h', dst='deps/openssl/openssl/include', src='%s/deps/openssl/openssl/include' % self.source_dir )
    self.copy( '*.h', dst='deps/openssl/openssl/crypto', src='%s/deps/openssl/openssl/crypto' % self.source_dir )
    self.copy( '*.h', dst='deps/openssl/config', src='%s/deps/openssl/config' % self.source_dir )
    self.copy( '*node*.lib', dst='lib', keep_path=False )
    self.copy( '*node*.dll', dst='bin', keep_path=False )
    self.copy( '*node*.so', dst='lib', keep_path=False )
    self.copy( '*node*.a', dst='lib', keep_path=False )

    if self.settings.build_type == 'Release':
      self.copy( '*node*.dylib', dst='lib', keep_path=False, src='%s/out/Release' % self.source_dir )

    if self.settings.build_type == 'Debug':
      self.copy( '*node*.dylib', dst='lib', keep_path=False, src='%s/out/Debug' % self.source_dir )

  def package_info( self ):
    self.cpp_info.includedirs = ['include', 'deps/v8', 'deps/v8/include', 'deps/uv/include', 'deps/cares/include', 'deps/openssl/openssl/include']
    self.cpp_info.libs = [ 'node' ]
