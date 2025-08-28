namespace app
{
    interface IPerson {
    void DisplayInformation();
    }
    class Student : IPerson

    {
        protected string StudentName;
        protected int StudentID;
        protected int age;

        public Student(string name, int id, int age)
        {
            this.StudentName = name;
            this.StudentID = id;
            this.age = age;
        }

        public string getName() { return this.StudentName; }
        public int getID() { return this.StudentID; }
        public int getAge() { return this.age; }

        public void setName(string input) { this.StudentName = input; }
        public void setID(int input) { this.StudentID = input; }
        public void getAge(int input) { this.age = input; }
        public virtual void DisplayInformation()
        {
            Console.WriteLine("Name:" + this.StudentName + ", ID:" + this.StudentID + ", Age:" + this.age);
        }

        public (string StudentName, int StudentId, int age) GetStudentInfo()
        {
            return (StudentName, StudentID, age);
        }


        }

    class CollegeStudent : Student
    {
        protected string major;
        protected float avgGrade;

        public CollegeStudent(string name, int id, int age, string major, float avgGrade) : base(name, id, age)
        {
            this.major = major;
            this.avgGrade = avgGrade;
        }

        public override void DisplayInformation()
        {
            base.DisplayInformation();
            Console.WriteLine("Major: " + this.major + ", Average Grade: " + this.avgGrade);
        }
    }
    class Program
    {
        static void Main(string[] args)
        {
            // new student

            //normal
            Student A = new Student("test", 123, 17);

            //college
            CollegeStudent B = new CollegeStudent("test", 123, 17, "CS", 96.5f);

            //changedata
            B.setName("Guy");
            A.setID(122512);

            var students = new List<Student> { A,B };
            foreach (var current in students)
            {
                current.DisplayInformation();
                Console.WriteLine();
            }
            
        }
    }
}

