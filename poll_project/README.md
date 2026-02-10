# 🗳️ Django Voting System

A modern, feature-rich web application for creating and managing polls with user authentication, advanced features, and a beautiful responsive UI.

- **Live Demo**: http://127.0.0.1:8000 (after running locally)
- **Repository**: [GitHub](https://github.com/yourusername/voting-system)

## ✨ Features

### 🔐 Authentication & User Management
- User registration with password validation
- Secure login/logout system
- User profiles with voting history
- Vote tracking and management

### 📊 Advanced Polling Features
- **Multiple Choice Voting** - Users can select multiple options on a single poll
- **Poll Categories/Tags** - Organize polls into categories
- **Poll Scheduling** - Set start and end dates for polls
- **Visibility Controls** - Public, private, and password-protected polls
- **Private Poll Invitations** - Invite specific users to private polls
- **Draft Polls** - Save polls as drafts before publishing
- **Poll Images** - Add featured images to polls
- **Choice Images** - Upload images for each poll choice
- **Poll Descriptions** - Detailed poll descriptions and choice explanations

### 💬 Community Features
- **Comments System** - Users can comment on polls
- **Comment Moderation** - Delete inappropriate comments
- **Vote Display** - See which choice you voted for in results

### 🔍 Search & Filtering
- Full-text search across poll questions and descriptions
- Filter by category, status (active/upcoming/expired)
- Real-time filtering with dropdowns

### 📈 Results & Analytics
- Interactive **Chart.js graphs** visualizing poll results
- Progress bars with vote percentages
- Vote count statistics
- Visual indicators for your votes

### 🎨 Modern UI/UX
- **Bootstrap 5** responsive framework
- **Dark Mode Toggle** - Switch between light and dark themes
- Mobile-optimized responsive design
- Smooth animations and transitions
- Modern badge and card layouts
- Status indicators (Active, Upcoming, Expired)

## 🛠️ Technology Stack

### Backend
- **Python 3.13.6**
- **Django 6.0.1** - Web framework
- **SQLite** - Database

### Frontend
- **Bootstrap 5.3.0** - CSS framework
- **Chart.js 4.4.0** - Interactive charts
- **HTML5 & CSS3**

### Libraries
- **Pillow** - Image processing
- **Django Built-in Auth** - User authentication

## 📋 System Requirements

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/voting-system.git
cd voting-system
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install django==6.0.1
pip install pillow
```

### 4. Apply Database Migrations
```bash
cd poll_project
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

### 6. Run Development Server
```bash
python manage.py runserver
```

The application will be available at **http://127.0.0.1:8000/**

## 📖 Usage

### For Users

#### Browse Polls
1. Visit the home page or `/polls/`
2. Use search bar and filters to find polls
3. Filter by category or poll status
4. Click "Vote Now!" on active polls

#### Vote on Polls
1. Select your choice(s)
2. For multiple-choice polls, select all applicable options
3. Click "Vote" or "Update Vote" to submit
4. View results with interactive charts

#### Create an Account & View History
1. Register at `/accounts/register/`
2. Log in at `/accounts/login/`
3. View your voting history at `/accounts/profile/`
4. See all polls you're invited to

#### Comment on Polls
1. Scroll to the comments section
2. Log in to post comments
3. Delete your own comments if needed

#### Toggle Dark Mode
1. Click the moon icon (🌙) in the top right navbar
2. Theme preference is saved automatically

### For Administrators

#### Access Admin Panel
1. Go to `/admin/`
2. Log in with superuser credentials

#### Create Polls
1. Click "Add Question"
2. Fill in poll details:
   - Question text and description
   - Upload featured image (optional)
   - Select category
   - Set start/end dates for scheduling
   - Choose visibility (public/private/password)
   - Enable multiple choice (optional)
   - Save as draft or publish
3. Add choices with descriptions and images

#### Manage Categories
1. Go to Categories section
2. Create, edit, or delete categories
3. Slugs are auto-generated for URL-friendly names

#### Invite Users to Private Polls
1. Create a private poll
2. In the "Invited Users" field, select users
3. Those users will see the poll in their results

#### Moderate Comments
1. Go to Comments section
2. View comments filtered by date or poll
3. Delete inappropriate comments

## 📁 Project Structure

```
poll_project/
├── manage.py
├── db.sqlite3
├── .gitignore
├── README.md
│
├── poll_project/              # Main project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── pollApp/                   # Main polling app
│   ├── models.py             # Core data models
│   ├── views.py              # Request handlers
│   ├── urls.py               # URL routing
│   ├── admin.py              # Admin configuration
│   └── migrations/           # Database migrations
│
├── accounts/                 # User authentication
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       ├── register.html
│       ├── login.html
│       └── profile.html
│
├── landingPage/              # Landing page app
│   ├── views.py
│   └── urls.py
│
├── templates/                # Template files
│   ├── base.html             # Base template with dark mode
│   ├── partials/
│   │   └── navbar.html       # Navigation bar
│   ├── accounts/
│   │   ├── register.html
│   │   ├── login.html
│   │   └── profile.html
│   ├── polls/
│   │   ├── index.html        # Poll listing
│   │   ├── detail.html       # Poll voting page
│   │   ├── results.html      # Results with charts
│   │   ├── category.html     # Category page
│   │   └── password.html     # Password prompt
│   └── pages/
│       └── index.html        # Home page
│
└── media/                    # User uploads
    ├── poll_images/
    └── choice_images/
```

## 🗄️ Database Models

### User (Django Built-in)
- username, email, password
- date_joined, is_active, is_staff

### Question (Poll)
- question_text, description
- category (ForeignKey)
- start_date, end_date (scheduling)
- visibility (public/private/password)
- password (for protected polls)
- image (featured image)
- allow_multiple_choices (boolean)
- is_draft (boolean)
- created_by (user), pub_date

### Choice
- choice_text, votes, image
- description, question (ForeignKey)

### Vote
- user (ForeignKey)
- choice (ForeignKey)
- voted_at (timestamp)
- Unique constraint: one vote per user per choice

### Category
- name, description, slug
- created_at (timestamp)

### Comment
- text, question (ForeignKey)
- user (ForeignKey)
- created_at, updated_at, is_edited

## 🎯 Key Functionality

### Poll Status Methods
```python
question.is_active()      # Poll is currently accepting votes
question.is_upcoming()    # Poll hasn't started yet
question.is_expired()     # Poll has ended
question.total_votes      # Total number of votes cast
```

### Access Control
- Creator of poll can always access their polls
- Invited users can access private polls they're invited to
- Password-protected polls accessible after entering correct password
- Public polls visible to all authenticated users

### Vote Management
- Users can change their vote anytime on active polls
- Vote counts update automatically
- Multiple choices can be selected on multiple-choice polls
- Unique constraint prevents duplicate votes

## 🌙 Dark Mode

The application includes a built-in dark mode toggle:
- Click the moon icon (🌙) in the navbar to switch themes
- Your preference is saved to browser localStorage
- Smooth transitions between light and dark modes
- All components are styled for both themes

## 📊 Chart Visualization

The results page includes an interactive Chart.js bar chart showing:
- Vote counts for each choice
- Color-coded bars for easy visualization
- Responsive design that adapts to screen size
- Traditional progress bars displayed below the chart

## 🔐 Security Features

- Password validation on registration
- CSRF protection on all forms
- Secure session-based authentication
- Password hashing with Django's built-in system
- Admin-only access controls
- User permission checks on all views

## 🧪 Testing

To test the application locally:

```bash
# Create admin user
python manage.py createsuperuser

# Create some categories
# Go to /admin/ and create categories

# Create test polls
# Use admin interface to create polls with various settings

# Test dark mode
# Click moon icon in navbar

# Test charts
# Create a poll with votes, view results page

# Test filtering
# Use search and filter dropdowns on /polls/
```

## 📝 API Endpoints

### User Authentication
- `accounts:register` - `/accounts/register/` - User registration
- `accounts:login` - `/accounts/login/` - User login
- `accounts:logout` - `/accounts/logout/` - User logout
- `accounts:profile` - `/accounts/profile/` - User profile

### Polls
- `polls:index` - `/polls/` - Poll listing with filters
- `polls:detail` - `/polls/<id>/` - Vote on poll
- `polls:results` - `/polls/<id>/results/` - View results
- `polls:category` - `/polls/category/<slug>/` - Category page
- `polls:vote` - `/polls/<id>/vote/` - Submit vote
- `polls:add_comment` - `/polls/<id>/comment/` - Add comment
- `polls:delete_comment` - `/polls/comment/<id>/delete/` - Delete comment

### Landing Page
- `index` - `/` - Home page

## 🚧 Future Enhancements

### Planned Features
1. **Poll Analytics Dashboard** - Visualize voting trends
2. **Export Results** - Download poll results as CSV/PDF
3. **Real-time Updates** - WebSocket support for live vote counts
4. **API REST Endpoints** - JSON API for mobile apps
5. **Email Notifications** - Alert users when invited to polls
6. **Poll Templates** - Create polls from templates
7. **Advanced Voting** - Ranked choice voting support
8. **Social Sharing** - Share polls on social media

## 🤝 Contributing

Contributions are welcome! Here's how to contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Bug Reports

Found a bug? Please create an issue on GitHub with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Django documentation and community
- Bootstrap framework
- Chart.js library
- Pillow image library
- All contributors and users

## 📚 Additional Resources

- [Django Official Documentation](https://docs.djangoproject.com/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/)
- [Chart.js Documentation](https://www.chartjs.org/docs/latest/)
- [Pillow Documentation](https://pillow.readthedocs.io/)

## 🎉 Getting Started

The quickest way to get started:

1. Clone the repo
2. Set up virtual environment
3. Install dependencies
4. Run migrations
5. Create superuser
6. Start server
7. Visit http://127.0.0.1:8000/

Happy voting! 🗳️

---

**Last Updated**: February 10, 2026
**Django Version**: 6.0.1
**Python Version**: 3.13.6
