def get_clientzone_html():
    return """
<!-- ClientZone Modal (Login + Portal) -->
<div id="clientzone-modal" class="fixed inset-0 z-50 overflow-y-auto hidden" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-center justify-center min-h-screen p-4">
        <div class="fixed inset-0 bg-brand-black/80 backdrop-blur-md transition-opacity" onclick="closeClientZone()"></div>
        <div class="bg-brand-slateBlack text-white rounded-3xl max-w-4xl w-full border border-white/10 relative z-10 shadow-2xl max-h-[90vh] overflow-y-auto">
            
            <!-- LOGIN VIEW (visible by default) -->
            <div id="cz-login-view" class="p-6 space-y-6">
                <div class="text-center space-y-2">
                    <div class="h-14 w-14 bg-brand-gold/10 text-brand-gold rounded-full flex items-center justify-center text-2xl mx-auto"><i class="fa-solid fa-user-shield"></i></div>
                    <h4 class="font-bold text-2xl text-white">ANGWA ClientZone</h4>
                    <p class="text-xs text-gray-400">Sign in to manage your services</p>
                </div>
                <div class="space-y-4 text-xs max-w-sm mx-auto">
                    <div>
                        <label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Email address</label>
                        <input type="email" id="cz-email" placeholder="client@example.com" class="w-full px-4 py-2.5 bg-brand-darkGray border border-white/10 rounded-xl text-white focus:ring-2 focus:ring-brand-gold">
                    </div>
                    <div>
                        <label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Password</label>
                        <input type="password" id="cz-password" placeholder="••••••••" class="w-full px-4 py-2.5 bg-brand-darkGray border border-white/10 rounded-xl text-white focus:ring-2 focus:ring-brand-gold">
                    </div>
                    <button onclick="submitClientZone()" class="w-full glossy-gold text-brand-black py-3 rounded-full font-bold uppercase tracking-wider text-xs">Sign in</button>
                    <div class="text-center text-[9px] text-gray-500">
                        No account? <button onclick="closeClientZone(); openRegisterModal()" class="text-brand-gold hover:underline">Create one</button>
                    </div>
                </div>
            </div>

            <!-- PORTAL VIEW (hidden until login) -->
            <div id="cz-portal-view" class="hidden p-6">
                <!-- Portal Header -->
                <div class="flex items-center justify-between border-b border-white/10 pb-4 mb-4">
                    <div class="flex items-center gap-3">
                        <div class="h-10 w-10 bg-brand-gold/15 rounded-full flex items-center justify-center text-brand-gold text-lg"><i class="fa-solid fa-user"></i></div>
                        <div>
                            <div class="font-bold text-white text-sm" id="cz-user-name">User</div>
                            <div class="text-[10px] text-gray-400" id="cz-user-email">user@example.com</div>
                        </div>
                    </div>
                    <button onclick="logoutClientZone()" class="text-xs text-gray-400 hover:text-red-400 transition-colors"><i class="fa-solid fa-sign-out-alt mr-1"></i> Logout</button>
                </div>

                <!-- Tabs -->
                <div class="flex border-b border-white/10 mb-6 text-xs font-bold uppercase tracking-wider">
                    <button class="cz-tab-btn px-4 py-2 text-brand-gold border-b-2 border-brand-gold" data-tab="dashboard">Dashboard</button>
                    <button class="cz-tab-btn px-4 py-2 text-gray-400 hover:text-white border-b-2 border-transparent" data-tab="orders">Orders</button>
                    <button class="cz-tab-btn px-4 py-2 text-gray-400 hover:text-white border-b-2 border-transparent" data-tab="profile">Profile</button>
                    <button class="cz-tab-btn px-4 py-2 text-gray-400 hover:text-white border-b-2 border-transparent" data-tab="support">Support</button>
                </div>

                <!-- Tab Content -->
                <div id="cz-tab-content" class="text-sm">
                    <!-- Dashboard -->
                    <div id="cz-dashboard" class="cz-tab-panel">
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                            <div class="bg-brand-darkGray/40 p-4 rounded-xl border border-white/5">
                                <div class="text-gray-400 text-[10px] uppercase">Active Services</div>
                                <div class="text-2xl font-bold text-brand-gold" id="cz-service-count">3</div>
                            </div>
                            <div class="bg-brand-darkGray/40 p-4 rounded-xl border border-white/5">
                                <div class="text-gray-400 text-[10px] uppercase">Total Orders</div>
                                <div class="text-2xl font-bold text-white" id="cz-order-count">5</div>
                            </div>
                            <div class="bg-brand-darkGray/40 p-4 rounded-xl border border-white/5">
                                <div class="text-gray-400 text-[10px] uppercase">Support Tickets</div>
                                <div class="text-2xl font-bold text-brand-green" id="cz-ticket-count">2</div>
                            </div>
                        </div>
                        <div class="bg-brand-darkGray/30 p-4 rounded-xl border border-white/5">
                            <h5 class="font-bold text-sm mb-2">Recent Activity</h5>
                            <ul class="space-y-2 text-xs text-gray-400">
                                <li class="flex justify-between border-b border-white/5 pb-2"><span>Order #1234 – Fibre 100Mbps</span><span class="text-brand-green">Completed</span></li>
                                <li class="flex justify-between border-b border-white/5 pb-2"><span>Order #1235 – Design Luxe</span><span class="text-brand-gold">In Progress</span></li>
                                <li class="flex justify-between"><span>Support ticket #56 – Billing</span><span class="text-gray-500">Open</span></li>
                            </ul>
                        </div>
                    </div>

                    <!-- Orders -->
                    <div id="cz-orders" class="cz-tab-panel hidden">
                        <div class="bg-brand-darkGray/30 p-4 rounded-xl border border-white/5">
                            <h5 class="font-bold text-sm mb-3">Order History</h5>
                            <div id="cz-orders-list" class="space-y-3 text-xs">
                                <!-- Dynamic orders will be inserted here -->
                                <div class="text-gray-400">Loading orders...</div>
                            </div>
                        </div>
                    </div>

                    <!-- Profile -->
                    <div id="cz-profile" class="cz-tab-panel hidden">
                        <div class="bg-brand-darkGray/30 p-4 rounded-xl border border-white/5 space-y-4">
                            <h5 class="font-bold text-sm">Edit Profile</h5>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                                <div>
                                    <label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Full Name</label>
                                    <input type="text" id="cz-profile-name" placeholder="Your name" class="w-full px-3 py-2 bg-brand-darkGray border border-white/10 rounded-lg text-white focus:ring-1 focus:ring-brand-gold">
                                </div>
                                <div>
                                    <label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Email</label>
                                    <input type="email" id="cz-profile-email" placeholder="email@example.com" class="w-full px-3 py-2 bg-brand-darkGray border border-white/10 rounded-lg text-white focus:ring-1 focus:ring-brand-gold" disabled>
                                </div>
                                <div>
                                    <label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Phone</label>
                                    <input type="tel" id="cz-profile-phone" placeholder="+27 12 345 6789" class="w-full px-3 py-2 bg-brand-darkGray border border-white/10 rounded-lg text-white focus:ring-1 focus:ring-brand-gold">
                                </div>
                                <div>
                                    <label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Address</label>
                                    <input type="text" id="cz-profile-address" placeholder="Your address" class="w-full px-3 py-2 bg-brand-darkGray border border-white/10 rounded-lg text-white focus:ring-1 focus:ring-brand-gold">
                                </div>
                            </div>
                            <button onclick="saveProfile()" class="glossy-gold text-brand-black px-6 py-2 rounded-full font-bold text-[10px] uppercase tracking-wider">Save Changes</button>
                        </div>
                    </div>

                    <!-- Support -->
                    <div id="cz-support" class="cz-tab-panel hidden">
                        <div class="bg-brand-darkGray/30 p-4 rounded-xl border border-white/5 space-y-4">
                            <h5 class="font-bold text-sm">Contact Support</h5>
                            <div class="space-y-3 text-xs">
                                <div>
                                    <label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Subject</label>
                                    <input type="text" id="cz-support-subject" placeholder="Brief issue summary" class="w-full px-3 py-2 bg-brand-darkGray border border-white/10 rounded-lg text-white focus:ring-1 focus:ring-brand-gold">
                                </div>
                                <div>
                                    <label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Message</label>
                                    <textarea id="cz-support-message" rows="4" placeholder="Describe your issue..." class="w-full px-3 py-2 bg-brand-darkGray border border-white/10 rounded-lg text-white focus:ring-1 focus:ring-brand-gold"></textarea>
                                </div>
                                <button onclick="submitSupportTicket()" class="glossy-green text-white px-6 py-2 rounded-full font-bold text-[10px] uppercase tracking-wider">Submit Ticket</button>
                            </div>
                            <div class="border-t border-white/10 pt-4 mt-4">
                                <h6 class="font-bold text-xs mb-2">Recent Tickets</h6>
                                <ul id="cz-support-tickets" class="space-y-2 text-xs text-gray-400">
                                    <li class="flex justify-between"><span>#56 – Billing issue</span><span class="text-brand-gold">Open</span></li>
                                    <li class="flex justify-between"><span>#55 – Installation delay</span><span class="text-brand-green">Resolved</span></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Close button (visible in both views) -->
            <div class="absolute top-4 right-4">
                <button onclick="closeClientZone()" class="text-gray-400 hover:text-white text-xl"><i class="fa-solid fa-circle-xmark"></i></button>
            </div>
        </div>
    </div>
</div>
"""
