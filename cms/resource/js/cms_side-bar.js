function sideBarActive(barIndex)
{
return  new Vue({
    el:'#side-bar',
    delimiters: ['${', '}'],
    mounted:function(){
      this.showActive();
    },
    methods:{
      showActive:function(){
        switch(barIndex){
          case 1:
                $($('#sidebar ul li')[1]).addClass('active');
                break;
          case 0:
                $($('#sidebar ul li')[0]).addClass('active');
                break;
          default:
                $($('#sidebar ul li')[0]).addClass('active')

        }
      }
    }
  })
}
