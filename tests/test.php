<?php echo 'hello'; ?><!DOCTYPE html>
<html>
  <head>
    <link    type  =  "text/css"       rel  =   "stylesheet" href = "main.css"  /> 
    <meta charset="utf-8">
    <title>wecomp</title>
    <script type = "text/javascript" src="main.js"   ></script   >
    <script>
      function foo ( bar ) {
        var foobar = 'foo ' + bar;
        return foobar;
      }
      alert ( foo ( 'hello world' ) ) ;
      
      // js inline comment
      /* js block comment */
      /*
      js block comment 
      */
      /**
       * js block comment
       */
    </script>
    <style>
      body { color: green; }
      
      div {
        border: 2em solid yellow;
        }
        
      .box {
        font-size: 30px;
        font-weight: bold;
        }
        
      #funnyDiv {
        background: red;
        }
        
      /* css comment */
    </style>
    <!-- html comment -->
  </head>
  <body>
    <div id="funnyDiv" class="box">
    
      <?= 'echo var var var' ?>
    
      Hello         
      
      <?php 
      echo 'hejoo!'; 
      
      ?>
      
      compression!
      
      <div id="<?= "echo var var var" ?>"></div>
      
    </div>
  </body>
</html>
      