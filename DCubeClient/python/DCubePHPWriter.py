#!/bin/env python
##
# @file DCubePHPWriter.py
# @author Krzyszotf Daniel Ciba (Krzysztof.Ciba@NOSPAMgmail.com)
# @brief implementation of DCubePHPWriter and test_DCubePHPWriter classes
#
#    DCube
#    Copyright (C) 2011  Krzysztof Ciba
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
import sys
import os
from time import strftime, localtime, strptime
from DCubeUtils import DCubeObject, DCubeException, DCubeVersion
from DCubeOptParser import DCubeOptParser 
import unittest
##
# @class DCubePHPWriter
# @author Krzysztof Daniel Ciba (Krzytof.Ciba@NOSPAMgmail.com) 
# @brief PHP files producer
class DCubePHPWriter( DCubeObject ):
    
    ## c'tor
    # @param self "My, myself and Irene"
    # @param parsed opts and args from DCubeOptParser
    def __init__( self, parsed ):
        super( DCubePHPWriter, self ).__init__( self )
        self.opts, self.args = parsed

        self.server = self.opts.server
        if ( not os.path.isdir( self.server ) ):
            self.server = os.path.dirname( self.server )

        self.debug( "server %s" % self.server )
        self.debug( "output %s" % os.path.dirname( os.path.abspath( self.opts.output ) ) )

        #self.server = self.__relpath( self.server, os.path.dirname(self.opts.output ) ) 

        #if ( self.server == "..") : self.server = "../"
        #self.server = "./" + self.server
        #self.info( "server relative path %s" % self.server )

        

    ## give relative path between target and base
    # @param self "Me, myself and Irene"
    # @param target target directory name
    # @param base base directory name
    def __relpath( self, target, base="." ):
   
        if ( not os.path.exists(target) ):
            self.error( "target directory %s does not exist" % target )

        if ( not os.path.isdir(base) ):
            self.warn( "base %s is not a directory or does not exist" % base )
        
 
        base_list = (os.path.abspath(base)).split(os.sep)
        target_list = (os.path.abspath(target)).split(os.sep)

        for i in range(min(len(base_list), len(target_list))):
            if base_list[i] <> target_list[i]: break
            else:
                i+=1

        rel_list = [os.pardir] * (len(base_list)-i) + target_list[i:]
        return os.path.join(*rel_list)
    
    ## php heading string
    # @param self "Me, myself and Irene"
    def __head( self ):
        return "<?php\n"

    ## php tail string
    # @param self "Me, myself and Irene"
    def __tail( self ):
        return "?>\n"

    ## php comment string
    # @param self "Me, myself and Irene"
    def __comment( self, what="output" ):
        
        out  = "/**\n"
        out += "  * DCubeClient PHP %s file\n" % what
        out += "  * autogenerated using %s\n" % DCubeVersion().version()
        out += "  * on %s\n" % strftime("%a, %d %b %Y %H:%M:%S %Z" , localtime())
        out += "  * Files:\n"
        out += "  * [1] monitored file  = %s\n" % str( self.opts.monitored )
        out += "  * [2] reference file  = %s\n" % str( self.opts.reference )
        out += "  * [3] config XML file = %s\n" % str( self.opts.config )
        out += "  * [4] output XML file = %s\n" % str( self.opts.output )
        out += "  * [5] log file        = %s\n" % str( self.opts.log )
        out += "  *\n"
        out += "  *  ***************************************************\n"
        out += "  *  *                   !!! WARNINIG !!!              *\n"
        out += "  *  * make sure that dcube.php is in PHP include path *\n"
        out += "  *  ***************************************************\n"
        out += "  *\n"
        out += "  *\n"
        out += "  *  ***************************************************\n"
        out += "  *  *                   !!! WARNINIG !!!              *\n"
        out += "  *  * make sure to put relative path from your result *\n"
        out += "  *  * directory to the the directory with dcube.php   *\n"
        out += "  *  ***************************************************\n"
        out += "  *\n" 
        
        return out

    ## body of output PHP file
    # @param self "Me, myself and Irene"
    def __bodyPHP( self ):
        out  = "/* ADD TO include_path TO LOCAL INSTALLATION OF DCUBE PHP PART */\n"
        out += "$where = \"%s\";\n" % self.server
        out += "set_include_path($where);\n";
        out += "require \"dcube.php\";\n\n";
 
        out += "$xml_file = \"%s\";\n" % os.path.basename(self.opts.output)
        out += "$log_file = \"%s\";\n" % os.path.basename(self.opts.log )
        out += "$dcube = new dcube( $xml_file, $log_file, $where );\n"
        return out

    ## body for log php file
    # @param self "Me, myself and Irene"
    def __bodyLOG( self ):
        out  = "/* ADD TO include_path TO LOCAL INSTALLATION OF DCUBE PHP PART */\n";
        out += "$where = \"%s\";\n" % self.server
        out += "set_include_path($where);\n"
        out += "require \"rw.php\";\n\n"
        out += "$log_file = \"%s\";\n" % os.path.basename(self.opts.log)
        out += "$page = new rainbow( $log_file );\n"
        return out

    ## dcube output PHP file contents 
    # @param self "Me, myself and Irene"
    def dcubePHP( self ):
        out  = self.__head()
        out += self.__comment()
        out += self.__bodyPHP()
        out += self.__tail()
        return out
        

    ## dcube log PHP file contents
    # @param self "Me, myself and Irene"
    def dcubeLOG( self ):
        out  = self.__head()
        out += self.__comment( "log" )
        out += self.__bodyLOG()
        out += self.__tail()
        return out
 

##
# @class test_DCubePHPWriter
# @author Krzysztof Daniel Ciba (Krzysztof.Ciba@NOSPAMgmail.com)
# @brief test case for DCubePHPWriter class
class test_DCubePHPWriter( unittest.TestCase ):

    ## test case setup
    # @param self "Me, myself and Irene"
    def setUp( self ):
        sys.argv = [__file__, "-r", "testRef.root", "-s", "/path/to/server/", "-x", "output.xml", "montitored.root" ]
        self.parsed  = DCubeOptParser().parse( sys.argv )
        self.parsed[0]._update_loose( { "monitored" : "monitored.root" } )

    ## c'tor
    # @param self "Me, myself and Irene"
    def test_01_ctor( self ):
        try:
            self.phpWriter = DCubePHPWriter( self.parsed )
        except:
            pass
        self.assertEqual( isinstance(self.phpWriter, DCubePHPWriter), True)


    ## dcubePHP  nad dcubeLOG
    # @param self "Me, myself and Irene"
    def test_02_writer( self ):
        phpWriter = DCubePHPWriter( self.parsed )
        print phpWriter.dcubePHP( )
        print phpWriter.dcubeLOG( )
    

## test suite execution
if __name__ == "__main__":
    testLoader = unittest.TestLoader()
    suite = testLoader.loadTestsFromTestCase(test_DCubePHPWriter)      
    unittest.TextTestRunner(verbosity=3).run(suite)

 

